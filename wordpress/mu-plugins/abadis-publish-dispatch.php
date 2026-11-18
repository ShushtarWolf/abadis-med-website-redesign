<?php
/**
 * Plugin Name: Abadis Publish Dispatch
 * Description: On publish, update, and unpublish/trash of posts, POST a signed repository_dispatch so GitHub Actions rebuilds the static site. Reads secrets from the environment. No credentials in this file.
 *
 * Install on abadis-wp-test: copy this file to wp-content/mu-plugins/abadis-publish-dispatch.php
 * Setup: see README.md in this directory.
 */

if (!defined('ABSPATH')) {
    exit;
}

function abadis_dispatch_env($name) {
    $value = getenv($name);
    if ($value === false || $value === '') {
        $value = defined($name) ? constant($name) : '';
    }
    return is_string($value) ? trim($value) : '';
}

function abadis_dispatch_lang() {
    $lang = abadis_dispatch_env('ABADIS_WP_LANG');
    if ($lang !== '') {
        return $lang;
    }
    if (function_exists('pll_current_language')) {
        $slug = pll_current_language('slug');
        if (is_string($slug) && $slug !== '') {
            return $slug;
        }
    }
    return 'fa';
}

function abadis_dispatch_sign($action, $post_id, $status, $lang, $ts, $secret) {
    $canonical = $action . "\n" . $post_id . "\n" . $status . "\n" . $lang . "\n" . $ts;
    return hash_hmac('sha256', $canonical, $secret);
}

function abadis_dispatch_send($action, $post) {
    if (!($post instanceof WP_Post) || $post->post_type !== 'post') {
        return;
    }
    if (wp_is_post_revision($post) || wp_is_post_autosave($post)) {
        return;
    }
    $secret = abadis_dispatch_env('ABADIS_WEBHOOK_SECRET');
    $token = abadis_dispatch_env('ABADIS_DISPATCH_TOKEN');
    $url = abadis_dispatch_env('ABADIS_DISPATCH_URL');
    if ($url === '') {
        $url = 'https://api.github.com/repos/ShushtarWolf/abadis-med-website-redesign/dispatches';
    }
    if ($secret === '' || $token === '') {
        return;
    }
    $lang = abadis_dispatch_lang();
    $ts = time();
    $status = (string) $post->post_status;
    $payload = array(
        'action' => $action,
        'post_id' => (int) $post->ID,
        'status' => $status,
        'slug' => (string) $post->post_name,
        'lang' => $lang,
        'modified_gmt' => (string) $post->post_modified_gmt,
        'ts' => $ts,
        'sig' => abadis_dispatch_sign($action, (int) $post->ID, $status, $lang, $ts, $secret),
    );
    $is_github = strpos($url, '://api.github.com/') !== false;
    $body = $is_github
        ? wp_json_encode(array('event_type' => 'wordpress-publish', 'client_payload' => $payload))
        : wp_json_encode($payload);
    $headers = array(
        'Content-Type' => 'application/json',
        'User-Agent' => 'abadis-publish-dispatch',
        'X-Abadis-Signature' => 'sha256=' . hash_hmac('sha256', $body, $secret),
    );
    if ($token !== '') {
        $headers['Authorization'] = 'Bearer ' . $token;
    }
    if ($is_github) {
        $headers['Accept'] = 'application/vnd.github+json';
        $headers['X-GitHub-Api-Version'] = '2022-11-28';
    }
    wp_remote_post($url, array(
        'timeout' => 8,
        'headers' => $headers,
        'body' => $body,
    ));
}

add_action('transition_post_status', function ($new, $old, $post) {
    if (!($post instanceof WP_Post) || $post->post_type !== 'post') {
        return;
    }
    if ($new === 'publish' && $old !== 'publish') {
        abadis_dispatch_send('publish', $post);
    } elseif ($new === 'publish' && $old === 'publish') {
        abadis_dispatch_send('update', $post);
    } elseif ($old === 'publish' && $new !== 'publish') {
        abadis_dispatch_send('unpublish', $post);
    }
}, 10, 3);

add_action('before_delete_post', function ($post_id) {
    $post = get_post($post_id);
    if ($post instanceof WP_Post && $post->post_type === 'post' && $post->post_status === 'publish') {
        abadis_dispatch_send('delete', $post);
    }
});
