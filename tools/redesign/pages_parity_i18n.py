"""Full EN and AR parity for Sustainable Development (SDGs), CSR (Save Zagros),
and C1 Careers Dashboard + 3 Culture Cards (Alireza voice note)."""
import re
from lib import esc, SITE
from layout import page, crumbs, section_mark
from pages_company import (
    sdgs_hero, sdg_icons, about_motion_tags, SLOGAN_CAREERS_I18N,
)


def build_arabic_sdgs(write):
    p = '../../'
    head_css, motion_js = about_motion_tags(p)
    hero = sdgs_hero(p, 'ar', 'التنمية <em>المستدامة</em>', crumbs(p, [('التنمية المستدامة', None)], lang='ar'))
    icons = sdg_icons('fa', p)
    body = f'''{hero}
  <section class="section sdg-page" id="sdg"><div class="wrap" style="max-width:980px">
    <div class="reveal" style="margin-top:34px;--i:0">
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px">
        {section_mark(p, "sdgs", "sec-mark--sm")}
        <h2 style="font-size:1.5rem;line-height:1.35;margin:0">وثيقة التزام شركة خزانات آباديس الطبية المعرفية بأهداف التنمية المستدامة للأمم المتحدة (UN SDGs)</h2>
      </div>
      <div class="prose">
        <p>تلتزم شركة <strong>خزانات آباديس الطبية</strong> المعرفية، بصفتها الشركة الرائدة والأولى في تصنيع <strong>أكياس الشفط ذات الاستخدام الواحد</strong> في إيران، بتوجيه أنشطتها الصناعية والبحثية بما يتوافق مع <strong>أهداف التنمية المستدامة للأمم المتحدة (UN SDGs)</strong>.<br>نحن نؤمن بأن التطور الصناعي لا يكتسب قيمته الحقيقية إلا عندما يقترن بالارتقاء بصحة المجتمع، و<strong>الحفاظ على الموارد الطبيعية، وتقليل الآثار البيئية، ونشر ثقافة الاستهلاك المسؤول</strong>.</p>
      </div>
    </div>
    <div class="reveal" style="margin-top:34px;--i:1">
      <h3 style="font-size:1.25rem;line-height:1.35;margin-bottom:12px">الأهداف الرئيسية والتوافق مع أهداف التنمية المستدامة (SDGs 3, 6, 7, 8, 9, 12, 13)</h3>
      {icons}
      <div class="prose">
        <ol class="sdg-goals">
          <li><strong>الصحة الجيدة والرفاه (SDG 3)</strong>
            <ul>
              <li>تعزيز سلامة المرضى والكوادر الطبية عبر القضاء على التلامس المباشر مع السوائل والإفرازات المعدية.</li>
              <li>الارتقاء بصحة بيئة المستشفيات والحد من مخاطر العدوى المكتسبة في المستشفيات (HAI) باستخدام فلاتر قطع التدفق الكارهة للماء بكفاءة ٩٩٫٩٩٩٪.</li>
            </ul>
          </li>
          <li><strong>المياه النظيفة والنظافة الصحية (SDG 6)</strong>
            <ul>
              <li>إلغاء عملية غسل خزانات الشفط التقليدية وتحقيق توفير كبير ومستدام في استهلاك المياه.</li>
              <li>توفير أكثر من <strong>١٢ مليون لتر من المياه سنوياً</strong> في ١٬٢٨٤ مركزاً علاجياً ومستشفى في جميع المحافظات الـ ٣١ (وأكثر من ٥٦٫٥ مليون لتر توفير تراكمي).</li>
            </ul>
          </li>
          <li><strong>طاقة نظيفة وبأسعار معقولة (SDG 7)</strong>
            <ul>
              <li>بإلغاء الحاجة إلى الغسل والتعقيم بالبخار والتجفيف للخزانات التقليدية، ينخفض استهلاك الطاقة الكهربائية والبخار والمواد الكيميائية المطهرة بشكل ملحوظ، مما يقلل البصمة الكربونية للمستشفيات.</li>
            </ul>
          </li>
          <li><strong>العمل اللائق ونمو الاقتصاد (SDG 8)</strong>
            <ul>
              <li>خلق فرص عمل تخصصية مستدامة في مجالات التصنيع، وضمان الجودة، والبحث والتطوير، والتصدير.</li>
              <li>تطوير الطاقة الإنتاجية السنوية إلى <strong>٥ ملايين كيس شفط ذي استخدام واحد سنوياً</strong>.</li>
            </ul>
          </li>
          <li><strong>الصناعة والابتكار والهياكل الأساسية (SDG 9)</strong>
            <ul>
              <li>توطين تقنية تصنيع أكياس الشفط وفلاتر قطع التدفق في إيران، وتوسيع الصادرات إلى أسواق <strong>العراق وعُمان وأوزبكستان وآسيا الوسطى</strong>.</li>
            </ul>
          </li>
          <li><strong>الاستهلاك والإنتاج المسؤولان (SDG 12)</strong>
            <ul>
              <li>استبدال العمليات المستهلكة للموارد بحلول مغلقة أكثر أماناً وكفاءة، وتنفيذ مشروع <strong>«معارض بلا كتالوجات ورقية»</strong> منذ عام ٢٠٢٢ عبر الكتالوجات الرقمية ورموز QR.</li>
            </ul>
          </li>
          <li><strong>العمل المناخي (SDG 13)</strong>
            <ul>
              <li>تنفيذ مشاريع المسؤولية الاجتماعية للشركات (CSR) وفي مقدمتها مبادرة <strong>«إنقاذ زاغروس الخضراء»</strong> لزراعة آلاف أشجار البلوط باسم المراكز العلاجية الشريكة لإحياء الغابات المتضررة.</li>
            </ul>
          </li>
        </ol>
      </div>
    </div>
    <div class="reveal" style="margin-top:34px;--i:2">
      <h3 style="font-size:1.25rem;line-height:1.35;margin-bottom:12px">الإنجازات المحققة والتزامات المستقبل</h3>
      <div class="prose">
        <ul>
          <li>خدمة <strong>١٬٢٨٤ مركزاً علاجياً نشطاً</strong> (١٬٢٤٢ مستشفى و٤٢ مركز جراحة) في جميع المحافظات الـ ٣١.</li>
          <li>توفير أكثر من <strong>١٢ مليون لتر من المياه سنوياً</strong> ومنع دخول آلاف اللترات من السوائل المعدية إلى شبكة الصرف الصحي.</li>
          <li>توظيف لوحات ذكاء الأعمال البيئية (Environmental BI) والذكاء الاصطناعي لقياس الأثر البيئي الفعلي في ترشيد الموارد.</li>
          <li>مواصلة تطوير المنتجات البوليمرية القابلة للتحلل والذوبان في الماء (PVA) لإدارة النفايات الطبية المستدامة.</li>
        </ul>
      </div>
    </div>
  </div></section>'''
    for rel, can in (('arabic/sdgs/index.html', 'arabic/sdgs/'), ('arabic/sustainability/index.html', 'arabic/sdgs/')):
        html = page(p, 'sdgs', 'التنمية المستدامة',
                    'وثيقة التزام شركة خزانات آباديس الطبية بأهداف التنمية المستدامة للأمم المتحدة (UN SDGs)',
                    body, lang='ar', fa_path='sdgs/', canonical_path=can,
                    extra_head=head_css, html_attrs='data-slogan="t1"', scripts=motion_js)
        write(rel, html)


def build_arabic_csr(write):
    p = '../../'
    body = f'''  <section class="page-hero">
    <div class="wrap page-hero-with-mark">
      <div class="page-hero-copy">
        {crumbs(p, [("المسؤولية الاجتماعية · إنقاذ زاغروس", None)], lang="ar")}
        <h1>إنقاذ زاغروس · <em>المسؤولية الاجتماعية لآباديس</em></h1>
        <p class="lead">غرس أشجار البلوط في مرتفعات زاغروس باسم المراكز العلاجية الشريكة؛ لنُحدث أثراً بقدر طرف إصبع لك، وللطبيعة، وللعالم.</p>
      </div>
      {section_mark(p, "zagros", "sec-mark--lg")}
    </div>
  </section>
  <section class="section"><div class="wrap">
    <div class="glass csr-stats reveal" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-bottom:28px;text-align:center">
      <div class="card" style="padding:20px"><strong style="display:block;font-size:1.75rem;color:var(--brand)">+٢٬٠٠٠</strong><span>شتلة بلوط مزروعة في غابات زاغروس</span></div>
      <div class="card" style="padding:20px"><strong style="display:block;font-size:1.75rem;color:var(--brand)">١٬٢٨٤</strong><span>مركز علاجي شريك في ٣١ محافظة</span></div>
      <div class="card" style="padding:20px"><strong style="display:block;font-size:1.75rem;color:var(--brand)">٨٠٠+</strong><span>مشارك في مؤتمر إنقاذ زاغروس</span></div>
    </div>
    <div class="card prose reveal" style="padding:26px;margin-bottom:24px">
      <h2>المسؤولية الاجتماعية لشركة خزانات آباديس الطبية</h2>
      <p>بصفتها أول وأكبر شركة مصنّعة لأكياس الشفط الطبية ذات الاستخدام الواحد في إيران، حرصت شركة خزانات آباديس الطبية المعرفية دائماً على أداء مسؤولياتها الاجتماعية والبيئية جنباً إلى جنب مع أنشطتها الصناعية والتجارية. نحن نؤمن بأن النجاح الحقيقي لا يتحقق إلا من خلال خلق قيمة مستدامة للمجتمع والطبيعة والأجيال القادمة.</p>
      <p>شملت مبادراتنا دعم المؤسسات الخيرية مثل «محك» و«كهريزك» وجمعية التوحد، وبناء المدارس في المناطق الأقل حظاً، وتكريم الكوادر التمريضية والطبية سنوياً في يوم التمريض وخلال جائحة كورونا.</p>
    </div>
    <div class="card prose reveal" style="padding:26px;margin-bottom:24px">
      <h2>مبادرة «إنقاذ زاغروس الخضراء» وغرس أشجار البلوط</h2>
      <p>تعد غابات زاغروس من أهم الذخائر البيئية ومصادر المياه الجوفية، وقد تعرضت خلال السنوات الماضية لحرائق وجفاف واسع. وانطلاقاً من التزامها البيئي، أطلقت آباديس بالتعاون مع مبادرة (Dpaper) مشروع غرس أشجار البلوط في مرتفعات زاغروس بعدد المراكز العلاجية الأعضاء في عائلة آباديس الخضراء (١٬٢٨٤ مركزاً علاجياً في ٣١ محافظة)، ليتم تسجيل غابة باسم آباديس وتخليداً لقطاع الرعاية الصحية.</p>
      <p>كما أقيم مؤتمر «إنقاذ زاغروس» بمشاركة نحو ٨٠٠ من النشطاء والخبراء البيئيين، وقام مديرو آباديس بزيارة رؤساء المستشفيات لتقديم لوحات شرف غرس أشجار البلوط باسم مستشفياتهم الرائدة في مكافحة العدوى.</p>
      <p><a class="btn btn-primary" href="{p}zagros-names/4-mix/">مشاهدة جدار الشرف لأسماء المستشفيات ({esc("١٬٢٨٤")} مركزاً)</a> <a class="btn btn-ghost" href="{p}arabic/customers/" style="margin-inline-start:8px">عائلة آباديس الخضراء</a></p>
    </div>
  </div></section>'''
    html = page(p, 'csr', 'المسؤولية الاجتماعية — إنقاذ زاغروس',
                'مبادرة إنقاذ زاغروس والمسؤولية الاجتماعية لشركة خزانات آباديس الطبية',
                body, lang='ar', fa_path='csr/', canonical_path='arabic/csr/')
    write('arabic/csr/index.html', html)


def build_c1_careers_i18n(write, lang, p='../../'):
    is_en = (lang == 'en')
    head_css, motion_js = about_motion_tags(p)
    lines = SLOGAN_CAREERS_I18N[lang]
    rot_spans = ''.join(
        f'<span class="co-slogan-line{" is-on" if i == 1 else ""}">{esc(lines[i])}</span>'
        for i in range(1, len(lines))
    )
    ico_acad = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'
    ico_bulb = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1v.2h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/></svg>'
    ico_team = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'

    if is_en:
        crumb_html = f'<p class="co-crumbs"><a href="{p}en/">Home</a> › Collaboration Opportunities</p>'
        h1_html = 'Collaboration <em>Opportunities</em>'
        motto = 'Together we learn, together we grow, and side by side we make an impact.'
        kpis = [
            (ico_acad, 'Abadis Academy', 'Specialized training and skill development alongside a clear career growth path'),
            (ico_bulb, 'Opportunity for Impact', 'A welcoming space where your ideas are heard, valued, and rewarded'),
            (ico_team, 'Young & Agile Culture', 'Dynamic spirit, close teamwork, and readiness for innovation and new experiences'),
        ]
        sec_h = 'Career Opportunities by Department'
        sec_p = 'Select your specialized department or submit your application to the Abadis General Talent Pool.'
        filters = [
            ('all', 'All Positions', '9'),
            ('active', 'Active Openings', '1'),
            ('rnd', 'R&D and Engineering', '1'),
            ('qa', 'Quality Assurance', '1'),
            ('sales', 'Sales & Commercial', '4'),
            ('finance', 'Finance & Admin', '3'),
        ]
        jobs = [
            ('sales', 'active', 'Sales & Commercial', 'Active', 'Sales Specialist (Account Executive)', 'Identify and onboard new healthcare centers, negotiate with hospitals, and manage orders in CRM.', 'Exp: 2+ yrs B2B / Medical Devices', 'Published: Oct 2026', 'sales-specialist'),
            ('rnd', 'archive', 'R&D and Engineering', 'Active Talent Pool', 'R&D Specialist', 'Develop innovative infection-control products, manage knowledge-based projects, and lead commercialization.', 'Exp: 4+ yrs related R&D', 'Talent Pool', 'rnd-specialist'),
            ('qa', 'archive', 'Quality Assurance', 'Active Talent Pool', 'Quality Assurance Specialist', 'Monitor ISO 13485 compliance, continuous production quality control, and IMED regulatory documentation.', 'Exp: 2+ yrs QA/QC', 'Talent Pool', 'quality-assurance'),
            ('sales', 'archive', 'Sales & Commercial', 'Active Talent Pool', 'Sales Manager', 'Lead nationwide hospital sales and provincial dealer network across all 31 provinces.', 'Exp: 10+ yrs Medical Devices', 'Talent Pool', 'sales-manager'),
            ('sales', 'archive', 'Sales & Commercial', 'Active Talent Pool', 'Export Specialist', 'Expand regional export markets (Iraq, Oman, Uzbekistan & Central Asia) and manage Incoterms logistics.', 'Exp: 3+ yrs International Trade', 'Talent Pool', 'export-specialist'),
            ('sales', 'archive', 'Sales & Commercial', 'Active Talent Pool', 'Market Research Specialist', 'Analyze hospital market trends, competitor intelligence, and customer satisfaction metrics.', 'Exp: 2+ yrs Market Research', 'Talent Pool', 'market-research'),
            ('finance', 'archive', 'Finance & Admin', 'Active Talent Pool', 'Accountant', 'Manage corporate accounting, hospital invoicing, tax filings, and financial reporting.', 'Exp: 3+ yrs Accounting', 'Talent Pool', 'accountant'),
            ('finance', 'archive', 'Finance & Admin', 'Active Talent Pool', 'Collections Officer', 'Follow up on hospital and distributor receivables and coordinate financial settlements.', 'Exp: 2+ yrs Finance/Collections', 'Talent Pool', 'collections-officer'),
            ('finance', 'archive', 'Finance & Admin', 'Active Talent Pool', 'Executive Secretary & Office Coordinator', 'Coordinate executive meetings, correspondence, and head-office administrative operations.', 'Exp: 2+ yrs Office Admin', 'Talent Pool', 'secretary'),
        ]
        apply_btn = 'Apply for This Role'
        detail_btn = 'Role Details'
        banner_h = 'General Talent Pool — Outside Current Openings'
        banner_p = 'If your specialty is not listed above, submit your résumé to our active talent pool for upcoming positions.'
        banner_cta = 'Submit General Application'
        form_h = 'Job Application & Résumé Submission Form'
        f_name, f_role, f_phone, f_email, f_exp, f_msg, f_send = 'Full Name', 'Target Role / Department', 'Mobile Phone', 'Email Address', 'Years of Experience & Education Summary', 'Cover Note / Key Skills', 'Submit Application'
    else:
        crumb_html = f'<p class="co-crumbs"><a href="{p}arabic/">الرئيسية</a> › فرص التعاون والعمل</p>'
        h1_html = 'فرص <em>التعاون والعمل</em>'
        motto = 'معاً نتعلم، معاً ننمو، وجنباً إلى جنب نُحدث الأثر.'
        kpis = [
            (ico_acad, 'أكاديمية آباديس', 'تدريب تخصصي وتطوير للمهارات مع مسار واضح للتقدم الوظيفي'),
            (ico_bulb, 'فرصة لإحداث الأثر', 'مساحة للاستماع إلى الأفكار والمشاركة وتقدير جهودك'),
            (ico_team, 'ثقافة مؤسسية شابة ومرنة', 'روح حيوية وتعاون وثيق واستعداد للابتكار والتجارب الجديدة'),
        ]
        sec_h = 'فرص العمل حسب الأقسام التنظيمية'
        sec_p = 'اختر القسم التخصصي المناسب لك أو سجّل في قاعدة السير الذاتية العامة لشركة آباديس.'
        filters = [
            ('all', 'كل الفرص', '٩'),
            ('active', 'الفرص النشطة', '١'),
            ('rnd', 'البحث والتطوير', '١'),
            ('qa', 'ضمان الجودة', '١'),
            ('sales', 'المبيعات والتجارة', '٤'),
            ('finance', 'المالية والإدارية', '٣'),
        ]
        jobs = [
            ('sales', 'active', 'المبيعات والتجارة', 'نشط', 'أخصائي مبيعات', 'استقطاب المراكز العلاجية الجديدة والتفاوض مع المستشفيات ومتابعة الطلبات في نظام CRM.', 'الخبرة: ٢+ سنة في المعدات الطبية', 'النشر: ١٤٠٥/٠٧/٠١', 'sales-specialist'),
            ('rnd', 'archive', 'البحث والتطوير', 'قاعدة السير الذاتية', 'أخصائي بحث وتطوير (R&D)', 'تطوير منتجات مكافحة العدوى الجديدة وإدارة المشاريع المعرفية والتسويق التجاري.', 'الخبرة: ٤+ سنوات مرتبطة', 'قاعدة المواهب', 'rnd-specialist'),
            ('qa', 'archive', 'ضمان الجودة', 'قاعدة السير الذاتية', 'أخصائي ضمان الجودة (QA)', 'متابعة معايير ISO 13485 والرقابة النوعية المستمرة لخطوط الإنتاج والتوثيق التنظيمي.', 'الخبرة: ٢+ سنة', 'قاعدة المواهب', 'quality-assurance'),
            ('sales', 'archive', 'المبيعات والتجارة', 'قاعدة السير الذاتية', 'مدير مبيعات', 'قيادة شبكة المبيعات والوكلاء في ٣١ محافظة ووضع استراتيجية التسويق الشاملة.', 'الخبرة: ١٠+ سنوات', 'قاعدة المواهب', 'sales-manager'),
            ('sales', 'archive', 'المبيعات والتجارة', 'قاعدة السير الذاتية', 'أخصائي تصدير', 'تطوير أسواق التصدير الإقليمية (العراق وعُمان وأوزبكستان) وإجراءات الشحن الدولية.', 'الخبرة: ٣+ سنوات', 'قاعدة المواهب', 'export-specialist'),
            ('sales', 'archive', 'المبيعات والتجارة', 'قاعدة السير الذاتية', 'أخصائي أبحاث السوق', 'تحليل اتجاهات سوق المستشفيات ومؤشرات رضا العملاء.', 'الخبرة: ٢+ سنة', 'قاعدة المواهب', 'market-research'),
            ('finance', 'archive', 'المالية والإدارية', 'قاعدة السير الذاتية', 'محاسب', 'إدارة الحسابات والفواتير والتقارير المالية والضريبية.', 'الخبرة: ٣+ سنوات', 'قاعدة المواهب', 'accountant'),
            ('finance', 'archive', 'المالية والإدارية', 'قاعدة السير الذاتية', 'مسؤول تحصيل المطالبات', 'متابعة التسويات المالية ومطالبات المراكز العلاجية والموزعين.', 'الخبرة: ٢+ سنة', 'قاعدة المواهب', 'collections-officer'),
            ('finance', 'archive', 'المالية والإدارية', 'قاعدة السير الذاتية', 'مسؤول مكتب وسكرتارية', 'تنسيق الاجتماعات والمراسلات والشؤون الإدارية للمكتب المركزي.', 'الخبرة: ٢+ سنة', 'قاعدة المواهب', 'secretary'),
        ]
        apply_btn = 'التقديم على هذه الفرصة'
        detail_btn = 'تفاصيل الوظيفة'
        banner_h = 'إرسال السيرة الذاتية العامة — خارج الوظائف المعلنة حالياً'
        banner_p = 'إذا لم يكن تخصصك ضمن القائمة أعلاه، يمكنك تسجيل سيرتك الذاتية في بنك المواهب للتواصل معك عند توفر شاغر مناسب.'
        banner_cta = 'إرسال سيرة ذاتية عامة'
        form_h = 'نموذج التقديم وإرسال السيرة الذاتية'
        f_name, f_role, f_phone, f_email, f_exp, f_msg, f_send = 'الاسم الكامل', 'الوظيفة المطلوبة / القسم', 'رقم الجوال', 'البريد الإلكتروني', 'سنوات الخبرة والمؤهل العلمي', 'نبذة عن المهارات والخبرات', 'إرسال الطلب'

    kpi_html = ''.join(
        f'<div class="co-kpi-pill"><div class="co-kpi-ico">{ico}</div>'
        f'<div class="co-kpi-txt"><strong>{esc(kt)}</strong><span>{esc(kd)}</span></div></div>'
        for ico, kt, kd in kpis
    )
    f_btns = ''.join(
        f'<button type="button" class="co-filter-btn{" is-active" if i == 0 else ""}" data-filter="{fk}">{esc(fl)} <span class="co-filter-count">{fc}</span></button>'
        for i, (fk, fl, fc) in enumerate(filters)
    )
    job_cards = ''.join(
        f'<article class="co-job-card{" is-active-job" if st == "active" else ""}" data-job-item data-dept="{dept}" data-status="{st}">'
        f'<div><div class="co-job-top"><span class="co-dept-tag">{esc(dlbl)}</span><span class="co-status-badge {"is-act" if st == "active" else "is-arc"}">{esc(slbl)}</span></div>'
        f'<h3>{esc(jtitle)}</h3><p class="co-job-summary">{esc(jsum)}</p></div>'
        f'<div><div class="co-job-meta"><span>{esc(jexp)}</span><span>{esc(jpub)}</span></div>'
        f'<div class="co-job-actions">'
        f'<a class="co-btn-apply" href="#apply" data-select-role="{esc(jtitle)}">{esc(apply_btn)}</a>'
        f'<a class="co-btn-detail" href="{p}careers/jobs/{jslug}/">{esc(detail_btn)}</a>'
        f'</div></div></article>'
        for dept, st, dlbl, slbl, jtitle, jsum, jexp, jpub, jslug in jobs
    )
    role_opts = ''.join(f'<option value="{esc(j[4])}">{esc(j[4])}</option>' for j in jobs)

    main = f'''  <section class="page-hero about-hero careers-hero co-hero has-playing-video">
    <video class="co-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-careers-poster.jpg?v=20261028p">
      <source src="{p}assets/media/hero-careers.mp4?v=20261028p" type="video/mp4">
    </video>
    <div class="co-wrap co-hero-grid">
      <div>
        {crumb_html}
        <h1>{h1_html}</h1>
        <p class="co-slogan" aria-label="{esc(" ".join(lines))}">
          <span class="co-slogan-main">{esc(lines[0])}</span>
          <span class="co-slogan-rotate" aria-hidden="true">{rot_spans}</span>
        </p>
        <p class="co-slogan-motto">{esc(motto)}</p>
      </div>
      <div class="co-hero-kpis">{kpi_html}</div>
    </div>
  </section>
  <section class="co-sec" id="jobs">
    <div class="co-wrap">
      <div class="co-sec-head"><div><h2>{esc(sec_h)}</h2><p>{esc(sec_p)}</p></div></div>
      <div class="co-filters" data-dept-filter role="tablist">{f_btns}</div>
      <div class="co-jobs-grid">{job_cards}</div>
      <div class="co-resume-banner" id="general-resume" style="margin-top:24px">
        <div><h3>{esc(banner_h)}</h3><p>{esc(banner_p)}</p></div>
        <a class="co-resume-cta" href="#apply">{esc(banner_cta)}</a>
      </div>
    </div>
  </section>
  <section class="co-sec co-sec--alt" id="apply">
    <div class="co-wrap">
      <form class="cf-card" data-abadis-form="careers" data-mailto-form="info@abadis-med.com" data-subject="Job Application — Abadis Med">
        <h2 style="margin:0 0 18px;font-size:1.35rem">{esc(form_h)}</h2>
        <div class="cf-grid-2">
          <label class="cf-lbl">{esc(f_name)}<input name="name" required autocomplete="name"></label>
          <label class="cf-lbl">{esc(f_role)}<select name="role" id="roleSelect"><option value="General Talent Pool">{esc(banner_cta)}</option>{role_opts}</select></label>
          <label class="cf-lbl">{esc(f_phone)}<input name="phone" type="tel" dir="ltr" required autocomplete="tel"></label>
          <label class="cf-lbl">{esc(f_email)}<input name="email" type="email" dir="ltr" autocomplete="email"></label>
          <label class="cf-lbl cf-col-span-2">{esc(f_exp)}<input name="experience" required></label>
          <label class="cf-lbl cf-col-span-2">{esc(f_msg)}<textarea name="msg" rows="4"></textarea></label>
        </div>
        <div style="margin-top:16px"><button type="submit" class="cf-btn-primary">{esc(f_send)}</button></div>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>
  <script>(function(){{
    var lines = document.querySelectorAll('.co-slogan-line');
    if (lines.length > 1) {{
      var idx = 0;
      setInterval(function(){{
        lines[idx].classList.remove('is-on');
        idx = (idx + 1) % lines.length;
        lines[idx].classList.add('is-on');
      }}, 2200);
    }}
    var fBtns = document.querySelectorAll('[data-dept-filter] [data-filter]');
    var cards = document.querySelectorAll('[data-job-item]');
    fBtns.forEach(function(b){{
      b.addEventListener('click', function(){{
        var k = b.getAttribute('data-filter');
        fBtns.forEach(function(x){{ x.classList.toggle('is-active', x === b); }});
        cards.forEach(function(c){{
          var match = (k === 'all') || (k === 'active' && c.getAttribute('data-status') === 'active') || (c.getAttribute('data-dept') === k);
          c.style.display = match ? '' : 'none';
        }});
      }});
    }});
    document.querySelectorAll('[data-select-role]').forEach(function(a){{
      a.addEventListener('click', function(){{
        var sel = document.getElementById('roleSelect');
        if (sel) sel.value = a.getAttribute('data-select-role');
      }});
    }});
  }})();</script>'''

    if is_en:
        for rel, can in (('en/collaboration-opportunities/index.html', 'en/collaboration-opportunities/'), ('en/careers/index.html', 'en/collaboration-opportunities/')):
            html = page(p, 'careers', 'Collaboration Opportunities', 'Career opportunities at Abadis Medical Reservoirs',
                        main, lang='en', fa_path='careers/', canonical_path=can,
                        extra_head=head_css, html_attrs='data-slogan="t1"', scripts=motion_js)
            write(rel, html)
    else:
        html = page(p, 'careers', 'فرص التعاون والعمل', 'فرص التعاون والعمل في شركة خزانات آباديس الطبية',
                    main, lang='ar', fa_path='careers/', canonical_path='arabic/careers/',
                    extra_head=head_css, html_attrs='data-slogan="t1"', scripts=motion_js)
        write('arabic/careers/index.html', html)


def build_all(write):
    build_arabic_sdgs(write)
    build_arabic_csr(write)
    build_c1_careers_i18n(write, 'en', '../../')
    build_c1_careers_i18n(write, 'ar', '../../')
