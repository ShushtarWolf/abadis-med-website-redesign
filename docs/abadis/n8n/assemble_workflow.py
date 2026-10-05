#!/usr/bin/env python3
"""Assemble Abadis audit v2 n8n Workflow SDK source from snippets."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNIP = ROOT / "snippets"
OUT = ROOT / "abadis-audit-v2.workflow.js"


def js(name: str) -> str:
    return (SNIP / name).read_text()


def q(name: str) -> str:
    return json.dumps(js(name))


AI_SYSTEM_DRAFT = (
    "You are the Abadis Med migration architect. Produce an evidence-based draft plan for Nuxt 4 + headless WordPress + Tailwind/Nuxt UI + Three.js/GLB + Liara + n8n. "
    "EVIDENCE RULES: Use ONLY the provided crawl/WP/export evidence. Do not invent URLs, CPT fields, plugins, forms, media, or business rules. "
    "LABELING (required on every major claim): FACT | INFERENCE | RECOMMENDATION | UNKNOWN/HUMAN REVIEW. "
    "If evidence is missing, write UNKNOWN/HUMAN REVIEW — never guess. Never recommend DELETE; use REVIEW. "
    "concept-preview/ is REJECTED CONCEPT — VISUAL REFERENCE ONLY (not approved design). "
    "REQUIRED SECTIONS (each with labels): "
    "1) SEO (titles/meta/canonical/robots/hreflang/schema/sitemap gaps) "
    "2) URL inventory & redirect map "
    "3) Content model & page types "
    "4) WordPress/CPTs/JetEngine public REST surface & totals (X-WP-Total) "
    "5) Multilingual architecture FA/EN/AR (lang attributes, discovery vs sitemap, Arabic lang issues) "
    "6) Media & documents (images alt/loading, PDFs, WP media) "
    "7) Forms & business functionality (actions/methods/fields, mailto/tel/WhatsApp) "
    "8) Product architecture & relationships (label INFERENCE clearly) "
    "9) Nuxt 4 frontend architecture "
    "10) Headless WordPress data/API strategy "
    "11) 3D/GLB handling "
    "12) Liara hosting/deploy "
    "13) Security "
    "14) Performance & caching headers observed "
    "15) Testing strategy "
    "16) Launch checklist "
    "17) Rollback plan "
    "Cite concrete evidence URLs/counts from the payload when stating FACTS."
)

AI_SYSTEM_QA = (
    "You are a strict QA reviewer of an Abadis Med migration draft. "
    "Return only findings: gaps, unsupported assumptions, contradictions, missing FACT labels, overconfident INFERENCES, "
    "and risks for SEO, URLs, multilingual FA/EN/AR, WordPress/CPTs, media, forms, product relationships, Nuxt 4, "
    "headless WP, 3D/GLB, Liara, security, performance, testing, launch, rollback. "
    "Label each finding FACT / INFERENCE / UNKNOWN/HUMAN REVIEW. Do not invent evidence. Do not rewrite the full plan."
)

AI_SYSTEM_FINAL = (
    "Synthesize the final Abadis Med migration master plan from EVIDENCE + DRAFT + QA. "
    "Every major statement must be labeled FACT, INFERENCE, RECOMMENDATION, or UNKNOWN/HUMAN REVIEW. "
    "No invented data. No DELETE recommendations. Preserve SEO equity, URLs, and media unless evidence forces REVIEW. "
    "concept-preview remains REJECTED CONCEPT — VISUAL REFERENCE ONLY. "
    "Deliver complete actionable coverage: SEO, URLs/redirects, content, WordPress/CPTs, multilingual FA/EN/AR, media, "
    "forms/business functionality, product architecture, Nuxt 4, headless WordPress, 3D/GLB, Liara, security, "
    "performance, testing, launch, and rollback. Include an open HUMAN REVIEW queue list for UNKNOWN items."
)


def main() -> None:
    code = f'''import {{ workflow, node, trigger, splitInBatches, nextBatch, ifElse, expr, newCredential }} from '@n8n/workflow-sdk';

const start = trigger({{
  type: 'n8n-nodes-base.manualTrigger',
  version: 1,
  config: {{ name: 'Manual Start', position: [0, 0] }},
}});

const config = node({{
  type: 'n8n-nodes-base.set',
  version: 3.4,
  config: {{
    name: 'Load Config',
    position: [220, 0],
    parameters: {{
      mode: 'manual',
      includeOtherFields: false,
      assignments: {{
        assignments: [
          {{ id: '1', name: 'baseUrl', type: 'string', value: 'https://abadis-med.com' }},
          {{ id: '2', name: 'maxCrawlUrls', type: 'number', value: 15 }},
          {{ id: '3', name: 'requestDelayMs', type: 'number', value: 800 }},
          {{ id: '4', name: 'userAgent', type: 'string', value: 'AbadisAuditBot/1.0 (+migration-audit)' }},
          {{ id: '5', name: 'runAi', type: 'boolean', value: true }},
          {{ id: '6', name: 'includeLanguageRoots', type: 'boolean', value: true }},
          {{ id: '7', name: 'wpPerPage', type: 'number', value: 50 }},
          {{ id: '8', name: 'maxBrokenLinkChecks', type: 'number', value: 20 }},
          {{ id: '9', name: 'wpMaxPagesPerEndpoint', type: 'number', value: 3 }},
        ],
      }},
    }},
  }},
}});

const initAudit = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Clear audit state',
    position: [440, 0],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('init.js')} }},
  }},
}});

const fetchRobots = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch robots.txt',
    position: [660, 0],
    parameters: {{
      method: 'GET',
      url: expr('={{{{ $json.baseUrl }}}}/robots.txt'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr('={{{{ $json.userAgent }}}}') }}] }},
      options: {{ timeout: 45000, response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'text' }} }} }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const storeRobots = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Store robots',
    position: [880, 0],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('store_robots.js')} }},
  }},
}});

const fetchSitemapIndex = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch sitemap index',
    position: [1100, 0],
    parameters: {{
      method: 'GET',
      url: expr('={{{{ $json.baseUrl }}}}/sitemap_index.xml'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr('={{{{ $json.userAgent }}}}') }}] }},
      options: {{ timeout: 60000, response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'text' }} }} }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const parseSitemapIndex = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Parse child sitemaps',
    position: [1320, 0],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('parse_sitemap_index.js')} }},
  }},
}});

const sitemapBatch = splitInBatches({{
  version: 3,
  config: {{ name: 'Batch child sitemaps', position: [1540, 0], parameters: {{ batchSize: 1 }} }},
}});

const fetchChildSitemap = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch child sitemap',
    position: [1760, -120],
    parameters: {{
      method: 'GET',
      url: expr('={{{{ $json.sitemapUrl }}}}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr('={{{{ $json.userAgent }}}}') }}] }},
      options: {{ timeout: 90000, response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'text' }} }} }},
    }},
    onError: 'continueRegularOutput',
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 1000,
  }},
}});

const extractSitemapUrls = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Extract sitemap URLs',
    position: [1980, -120],
    parameters: {{ mode: 'runOnceForEachItem', language: 'javaScript', jsCode: {q('extract_sitemap.js')} }},
  }},
}});

const waitSitemap = node({{
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {{
    name: 'Throttle sitemaps',
    position: [2200, -120],
    parameters: {{ resume: 'timeInterval', amount: 1, unit: 'seconds' }},
  }},
}});

const fetchWpRoot = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch wp-json root',
    position: [1760, 160],
    parameters: {{
      method: 'GET',
      url: expr("={{{{ $('Load Config').first().json.baseUrl }}}}/wp-json/"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr("={{{{ $('Load Config').first().json.userAgent }}}}") }}] }},
      options: {{ timeout: 90000, response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'json' }} }} }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const fetchWpTypes = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch WP types',
    position: [1980, 160],
    parameters: {{
      method: 'GET',
      url: expr("={{{{ $('Load Config').first().json.baseUrl }}}}/wp-json/wp/v2/types"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr("={{{{ $('Load Config').first().json.userAgent }}}}") }}] }},
      options: {{ timeout: 90000, response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'json' }} }} }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const fetchWpTaxonomies = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch WP taxonomies',
    position: [2200, 160],
    parameters: {{
      method: 'GET',
      url: expr("={{{{ $('Load Config').first().json.baseUrl }}}}/wp-json/wp/v2/taxonomies"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr("={{{{ $('Load Config').first().json.userAgent }}}}") }}] }},
      options: {{ timeout: 90000, response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'json' }} }} }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const buildWpEndpoints = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Build WP endpoints',
    position: [2420, 160],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('build_wp_endpoints.js')} }},
  }},
}});

const wpBatch = splitInBatches({{
  version: 3,
  config: {{ name: 'Batch WP endpoints', position: [2640, 160], parameters: {{ batchSize: 1 }} }},
}});

const fetchWpEndpoint = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch WP endpoint pages',
    position: [2860, 80],
    parameters: {{
      method: 'GET',
      url: expr('={{{{ $json.endpointUrl }}}}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr('={{{{ $json.userAgent }}}}') }}] }},
      sendQuery: true,
      queryParameters: {{ parameters: [{{ name: 'page', value: '1' }}] }},
      options: {{
        timeout: 120000,
        response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'json' }} }},
        pagination: {{
          pagination: {{
            paginationMode: 'updateAParameterInEachRequest',
            parameters: {{ parameters: [{{ type: 'qs', name: 'page', value: '={{{{ $pageCount + 1 }}}}' }}] }},
            paginationCompleteWhen: 'other',
            completeExpression: '={{{{ Number($response.headers["x-wp-totalpages"] || $response.headers["X-WP-TotalPages"] || 1) <= $pageCount + 1 }}}}',
            limitPagesFetched: true,
            maxRequests: expr('={{{{ Number($json.wpMaxPagesPerEndpoint || 3) }}}}'),
            requestInterval: 800,
          }},
        }},
      }},
    }},
    onError: 'continueRegularOutput',
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 1000,
  }},
}});

const storeWpPage = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Store WP content page',
    position: [3080, 80],
    parameters: {{ mode: 'runOnceForEachItem', language: 'javaScript', jsCode: {q('store_wp_page.js')} }},
  }},
}});

const enArSeed = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Seed EN AR roots',
    position: [2860, 280],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('en_ar_seed.js')} }},
  }},
}});

const enArBatch = splitInBatches({{
  version: 3,
  config: {{ name: 'Batch EN AR seeds', position: [3080, 280], parameters: {{ batchSize: 1 }} }},
}});

const fetchEnAr = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch EN AR root',
    position: [3300, 200],
    parameters: {{
      method: 'GET',
      url: expr('={{{{ $json.crawlUrl }}}}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr('={{{{ $json.userAgent }}}}') }}] }},
      options: {{
        timeout: 90000,
        redirect: {{ redirect: {{ followRedirects: true, maxRedirects: 5 }} }},
        response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'text' }} }},
      }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const extractEnAr = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Extract EN AR links',
    position: [3520, 200],
    parameters: {{ mode: 'runOnceForEachItem', language: 'javaScript', jsCode: {q('en_ar_extract.js')} }},
  }},
}});

const waitEnAr = node({{
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {{
    name: 'Throttle EN AR',
    position: [3740, 200],
    parameters: {{ resume: 'timeInterval', amount: 1, unit: 'seconds' }},
  }},
}});

const buildCrawl = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Build crawl list',
    position: [3300, 400],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('build_crawl.js')} }},
  }},
}});

const pageBatch = splitInBatches({{
  version: 3,
  config: {{ name: 'Batch page crawl', position: [3520, 400], parameters: {{ batchSize: 1 }} }},
}});

const waitPage = node({{
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {{
    name: 'Throttle pages',
    position: [3740, 320],
    parameters: {{ resume: 'timeInterval', amount: 1, unit: 'seconds' }},
  }},
}});

const resolveRedirects = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Resolve redirect chain',
    position: [3960, 320],
    parameters: {{ mode: 'runOnceForEachItem', language: 'javaScript', jsCode: {q('resolve_redirects.js')} }},
  }},
}});

const fetchPage = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Fetch page HTML',
    position: [4180, 320],
    parameters: {{
      method: 'GET',
      url: expr("={{{{ $json.finalUrl || $json.crawlUrl }}}}"),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr("={{{{ $('Load Config').first().json.userAgent }}}}") }}] }},
      options: {{
        timeout: 90000,
        redirect: {{ redirect: {{ followRedirects: true, maxRedirects: 5 }} }},
        response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'text' }} }},
      }},
    }},
    onError: 'continueRegularOutput',
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 1000,
    alwaysOutputData: true,
  }},
}});

const analyzePage = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Analyze page SEO',
    position: [4400, 320],
    parameters: {{ mode: 'runOnceForEachItem', language: 'javaScript', jsCode: {q('analyze_page.js')} }},
  }},
}});

const collectLinks = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Collect internal links',
    position: [3960, 520],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('collect_links.js')} }},
  }},
}});

const linkBatch = splitInBatches({{
  version: 3,
  config: {{ name: 'Batch link checks', position: [4180, 520], parameters: {{ batchSize: 1 }} }},
}});

const waitLink = node({{
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {{
    name: 'Throttle links',
    position: [4400, 440],
    parameters: {{ resume: 'timeInterval', amount: 1, unit: 'seconds' }},
  }},
}});

const checkLink = node({{
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {{
    name: 'Check broken link',
    position: [4620, 440],
    parameters: {{
      method: 'HEAD',
      url: expr('={{{{ $json.skip ? $(\\'Load Config\\').first().json.baseUrl : $json.linkUrl }}}}'),
      authentication: 'none',
      sendHeaders: true,
      headerParameters: {{ parameters: [{{ name: 'User-Agent', value: expr('={{{{ $json.userAgent }}}}') }}] }},
      options: {{
        timeout: 30000,
        redirect: {{ redirect: {{ followRedirects: true, maxRedirects: 5 }} }},
        response: {{ response: {{ fullResponse: true, neverError: true, responseFormat: 'text' }} }},
      }},
    }},
    onError: 'continueRegularOutput',
    alwaysOutputData: true,
  }},
}});

const storeLink = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Store link check',
    position: [4840, 440],
    parameters: {{ mode: 'runOnceForEachItem', language: 'javaScript', jsCode: {q('store_link_check.js')} }},
  }},
}});

const relationships = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Orphans and relationships',
    position: [4620, 620],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('relationships.js')} }},
  }},
}});

const normalize = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Normalize evidence',
    position: [4840, 620],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('normalize.js')} }},
  }},
}});

const aiGate = ifElse({{
  version: 2.2,
  config: {{
    name: 'AI enabled?',
    position: [5060, 620],
    parameters: {{
      conditions: {{
        options: {{ caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 }},
        conditions: [{{ id: 'c1', leftValue: expr('={{{{ $json.runAi }}}}'), rightValue: true, operator: {{ type: 'boolean', operation: 'true', singleValue: true }} }}],
        combinator: 'and',
      }},
    }},
  }},
}});

const aiDraft = node({{
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {{
    name: 'AI Draft Plan',
    position: [5280, 500],
    credentials: {{ openAiApi: newCredential('OpenAI Gateway') }},
    parameters: {{
      resource: 'text',
      operation: 'response',
      modelId: {{ __rl: true, mode: 'id', value: 'gpt-4.1-mini' }},
      responses: {{ values: [
        {{ type: 'text', role: 'system', content: {json.dumps(AI_SYSTEM_DRAFT)} }},
        {{ type: 'text', role: 'user', content: expr('={{{{ $json.evidenceSummary }}}}') }},
      ] }},
      simplify: true,
      options: {{ maxTokens: 4500 }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const attachDraft = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Attach draft plan',
    position: [5500, 500],
    parameters: {{
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: "const base = $('Normalize evidence').first().json;\\nconst draft = items[0].json.text || items[0].json.output || items[0].json.content || JSON.stringify(items[0].json);\\nreturn [{{ json: {{ ...base, draftPlan: draft, evidenceSummary: base.evidenceSummary + '\\\\n\\\\n--- DRAFT PLAN ---\\\\n' + String(draft).slice(0, 50000) }} }}];",
    }},
  }},
}});

const aiQa = node({{
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {{
    name: 'AI QA Review',
    position: [5720, 500],
    credentials: {{ openAiApi: newCredential('OpenAI Gateway') }},
    parameters: {{
      resource: 'text',
      operation: 'response',
      modelId: {{ __rl: true, mode: 'id', value: 'gpt-4.1-mini' }},
      responses: {{ values: [
        {{ type: 'text', role: 'system', content: {json.dumps(AI_SYSTEM_QA)} }},
        {{ type: 'text', role: 'user', content: expr('={{{{ $json.evidenceSummary }}}}') }},
      ] }},
      simplify: true,
      options: {{ maxTokens: 3000 }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const attachQa = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Attach QA findings',
    position: [5940, 500],
    parameters: {{
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: "const base = $('Attach draft plan').first().json;\\nconst qa = items[0].json.text || items[0].json.output || items[0].json.content || JSON.stringify(items[0].json);\\nreturn [{{ json: {{ ...base, qaFindings: qa, evidenceSummary: base.evidenceSummary + '\\\\n\\\\n--- QA FINDINGS ---\\\\n' + String(qa).slice(0, 40000) }} }}];",
    }},
  }},
}});

const aiFinal = node({{
  type: '@n8n/n8n-nodes-langchain.openAi',
  version: 2.3,
  config: {{
    name: 'AI Final Plan',
    position: [6160, 500],
    credentials: {{ openAiApi: newCredential('OpenAI Gateway') }},
    parameters: {{
      resource: 'text',
      operation: 'response',
      modelId: {{ __rl: true, mode: 'id', value: 'gpt-4.1-mini' }},
      responses: {{ values: [
        {{ type: 'text', role: 'system', content: {json.dumps(AI_SYSTEM_FINAL)} }},
        {{ type: 'text', role: 'user', content: expr('={{{{ $json.evidenceSummary }}}}') }},
      ] }},
      simplify: true,
      options: {{ maxTokens: 5000 }},
    }},
    onError: 'continueRegularOutput',
  }},
}});

const packExports = node({{
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {{
    name: 'Pack export payloads',
    position: [6380, 620],
    parameters: {{ mode: 'runOnceForAllItems', language: 'javaScript', jsCode: {q('pack.js')} }},
  }},
}});

const exportFiles = node({{
  type: 'n8n-nodes-base.convertToFile',
  version: 1.1,
  config: {{
    name: 'Convert exports to files',
    position: [6600, 620],
    parameters: {{
      operation: 'toText',
      sourceProperty: 'content',
      binaryPropertyName: 'data',
      options: {{ fileName: expr('={{{{ $json.fileName }}}}'), mimeType: expr('={{{{ $json.mimeType }}}}') }},
    }},
  }},
}});

export default workflow('abadis-website-audit-v2', 'Abadis Website Audit v2')
  .add(start)
  .to(config)
  .to(initAudit)
  .to(fetchRobots)
  .to(storeRobots)
  .to(fetchSitemapIndex)
  .to(parseSitemapIndex)
  .to(sitemapBatch.onEachBatch(fetchChildSitemap.to(extractSitemapUrls).to(waitSitemap).to(nextBatch(sitemapBatch))).onDone(fetchWpRoot))
  .to(fetchWpTypes)
  .to(fetchWpTaxonomies)
  .to(buildWpEndpoints)
  .to(wpBatch.onEachBatch(fetchWpEndpoint.to(storeWpPage).to(nextBatch(wpBatch))).onDone(enArSeed))
  .to(enArBatch.onEachBatch(fetchEnAr.to(extractEnAr).to(waitEnAr).to(nextBatch(enArBatch))).onDone(buildCrawl))
  .to(pageBatch.onEachBatch(waitPage.to(resolveRedirects).to(fetchPage).to(analyzePage).to(nextBatch(pageBatch))).onDone(collectLinks))
  .to(linkBatch.onEachBatch(waitLink.to(checkLink).to(storeLink).to(nextBatch(linkBatch))).onDone(relationships))
  .to(normalize)
  .to(aiGate.onTrue(aiDraft.to(attachDraft).to(aiQa).to(attachQa).to(aiFinal.to(packExports.to(exportFiles)))).onFalse(packExports.to(exportFiles)))
  .group('Load configuration', [config, initAudit], {{ description: 'Sets audit config and clears prior run state every execution' }})
  .group('Discover site maps', [fetchRobots, storeRobots, fetchSitemapIndex, parseSitemapIndex], {{ description: 'Loads robots and parses the sitemap index into child sitemap URLs' }})
  .group('AI plan stages', [aiDraft, attachDraft, aiQa, attachQa, aiFinal], {{ description: 'Draft, QA, and final evidence-based migration plan via Gateway OpenAI' }});
'''
    # Fix over-escaped expr templates: assembler used {{{{ which becomes {{{{ in output
    # We want {{ in the SDK file for expr('={{ ... }}')
    code = code.replace('{{{{', '{{').replace('}}}}', '}}')
    # But json.dumps and f-string already handled most - the expr ones used {{{{ intentionally
    # After replace, expr('={{ $json.baseUrl }}') is correct
    # Double-check escaped quotes in fetchPage URL
    OUT.write_text(code)
    print(f'Wrote {OUT} ({OUT.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
