// Portfolio translations — German is the HTML default; English applied via JS
const TRANSLATIONS = {
  de: {
    // Navigation
    'nav-home': 'Startseite',
    'nav-application': 'Bewerbungsportfolio',
    'nav-academic': 'Wissenschaftliche Arbeiten',
    'nav-projects': 'Projekte',
    'nav-contact': 'Kontakt',

    // Index hero
    'hero-subtitle': 'Data Scientist | Quantitative Analyse gesellschaftlicher Datenbestände',
    'hero-desc': 'Ich entwickle reproduzierbare Analyseworkflows für gesellschaftlich relevante Fragestellungen: von der Datenaufbereitung und statistischen Modellierung über maschinelles Lernen bis zur zielgruppengerechten Ergebnisvermittlung.',
    'hero-btn-projects': 'Relevante Projekte ansehen',
    'hero-btn-cv': 'Lebenslauf herunterladen',
    'hero-btn-methods': 'Methoden & Erfahrung',

    // Profile snapshot
    'profile-heading': 'Profil in Kürze',
    'profile-subtext': 'Vier nachweisbare Kompetenzbereiche, jeder belegt durch abgeschlossene Projekte, begutachtete Arbeiten oder mehrjährige Forschungstätigkeit.',
    'rfcard1-title': 'Quantitative Modellierung',
    'rfcard1-body': 'Kausalinferenz (RDD, DiD, PSM), Bayes-Ökonometrie, Paneldaten, Verteilungsregression und Monte-Carlo-Simulation, belegt durch begutachtete Abschlussarbeiten (Note 1,0) und eigenständige Forschungsprojekte.',
    'rfcard2-title': 'Python, R, Stata & reproduzierbare Pipelines',
    'rfcard2-body': 'Vier Jahre Anwendungspraxis mit pandas, scikit-learn, matplotlib, tidyverse und ggplot2, eingesetzt mit Git, Makefile, pytest und vollständig dokumentierten Analyseworkflows.',
    'rfcard3-title': 'Öffentliche Verwaltungs- und Politikdaten',
    'rfcard3-body': 'Analyse offizieller Bundesstatistiken (BMI/BKA) und parlamentarischer Protokolldaten, mit konsequenter Quelldokumentation, Prüfsummenvalidierung und expliziten Interpretationsgrenzen.',
    'rfcard4-title': 'Adressatengerechte Kommunikation',
    'rfcard4-body': 'Visualisierungen, kompakte Ergebniszusammenfassungen und Berichte für Forschende, Entscheidungsträger und Nicht-Fachpublikum, in akademischen und institutionellen Kontexten.',

    // Selected projects section
    'projects-heading': 'Ausgewählte Datenprojekte',
    'projects-subtext': 'Angewandte Fallstudien zu öffentlichen Verwaltungsdaten, amtlichen Sicherheitsstatistiken, kausaler Politikanalyse und reproduzierbaren Machine-Learning-Workflows.',

    'proj-pmk-title': 'Politisch Motivierte Kriminalität: Öffentliches Datenanalyse-Dashboard',
    'proj-pmk-status': 'Vollständige Analyse',
    'proj-pmk-desc': 'Dokumentierter Analyseworkflow für amtliche PMK-Aggregatdaten aus BMI/BKA-Publikationen (2022–2024): prüfsummenvalidierter Datensatz, vier reproduzierbare Visualisierungen, vollständige Quellendokumentation und explizite Interpretationsgrenzen.',
    'demonstrates-label': 'Demonstriert:',
    'proj-pmk-demonstrates': 'Quelldokumentation, Prüfsummenvalidierung und nüchterne Visualisierung amtlicher Verwaltungsstatistiken. Jede Zahl ist einer konkreten Quelle zugeordnet.',
    'proj-pmk-btn': 'Zum Projekt',

    'proj-bfv-title': 'BfV Verfassungsschutzberichte: Öffentliche Aggregatdaten',
    'proj-bfv-status': 'Validiertes MVP',
    'proj-bfv-desc': 'Dokumentierter Analyseworkflow für amtliche BfV-Aggregatstatistiken aus Verfassungsschutzberichten 2022–2024: Personalpotenzial nach Phänomenbereich (Rechtsextremismus: 50.250 in 2024), extremistisch motivierte Straftaten, 8/8 Konsistenzprüfungen bestanden, vollständige Quellendokumentation auf URL-Ebene.',
    'proj-bfv-demonstrates': 'Strukturierte Extraktion öffentlicher Sicherheitsstatistiken, systematische Quelldokumentation auf URL-Ebene, reproduzierbare Datenpipeline auf amtlichen BfV-Aggregatdaten.',
    'proj-bfv-btn': 'Zum Projekt',

    'proj-causal-title': 'Kausale Politikanalyse mit quasi-experimentellen Methoden',
    'proj-causal-status': 'Begutachtete Forschungsarbeit',
    'proj-causal-desc': 'Zwei abgeschlossene, benotete Analysen mit RDD und DiD: Uruguay PANES-Programm (ca. 10 % kausaler Anstieg politischer Unterstützung; Note: Distinction 83 %) und COVID-19-Lockdown und Lebenszufriedenheit (DiD + PSM, HILDA-Panel, 215.000 Beobachtungen).',
    'proj-causal-demonstrates': 'Kausales Schlussfolgern jenseits von Korrelation. Identifikationsstrategie, Annahmentests, Robustheitsprüfungen und transparente Unsicherheitskommunikation für politikrelevante Fragen.',
    'proj-causal-btn': 'Zum Projekt',

    'proj-ml-title': 'Reproduzierbare Machine-Learning-Pipeline',
    'proj-ml-status': 'Ingenieurtechnischer Nachweis',
    'proj-ml-desc': 'End-to-End-Supervised-Learning-Workflow: leckagefreie sklearn-Pipelines, Modellvergleich (LR, RF, GBM), Kreuzvalidierung, 11 automatisierte pytest-Tests und reproduzierbare Dokumentation. Random Forest: ROC-AUC 0,900.',
    'proj-ml-demonstrates': 'Saubere Python-Projektstruktur, Vermeidung von Data Leakage, Modellvalidierung, automatisierte Tests und reproduzierbare Ergebnisdokumentation.',
    'proj-ml-btn': 'Zum Projekt',

    'proj-all-btn': 'Alle Projekte ansehen',

    // Tools
    'tools-heading': 'Werkzeuge & Methoden',

    // Responsible data
    'resp-heading': 'Verantwortungsvoller Umgang mit gesellschaftlich sensiblen Daten',
    'resp-subtext': 'Analytische Belastbarkeit erfordert nicht nur methodische Sorgfalt, sondern auch verantwortungsvolle Interpretation, insbesondere bei Daten mit gesellschaftlicher Sprengkraft. Diese Grundsätze leiten meine gesamte Arbeit.',

    // Experience
    'exp-heading': 'Berufliche Erfahrung in der Datenanalyse',

    // Academic background
    'acad-bg-heading': 'Akademischer Hintergrund',
    'acad-bg-cv-btn': 'Lebenslauf herunterladen',

    // Academic works (index)
    'acad-works-heading': 'Ausgewählte wissenschaftliche Arbeiten',
    'acad-works-all-btn': 'Alle wissenschaftlichen Arbeiten',

    // CTA
    'cta-heading': 'Meine Arbeiten erkunden',
    'cta-desc': 'Angewandte Datenprojekte mit reproduzierbarem Code und dokumentierten Pipelines, sowie quantitative Forschungsarbeiten zu statistischer Theorie, Ökonometrie und kausaler Inferenz.',
    'cta-btn-projects': 'Projekte ansehen',
    'cta-btn-application': 'Bewerbungsportfolio',
    'cta-btn-contact': 'Kontakt',

    // Footer
    'footer-copyright': '© 2026 Jonathan Gödeke. Alle Rechte vorbehalten.',
    'footer-cv': 'Lebenslauf herunterladen',

    // --- Projects page ---
    'page-projects-hero-title': 'Angewandte Data-Science-Projekte',
    'page-projects-hero-desc': 'Ausgewählte Fallstudien, die meinen analytischen Ansatz dokumentieren: Fragestellung, Datenaufbereitung, Modellierung, Validierung, Visualisierung und reproduzierbare Workflows auf öffentlichen, institutionellen und administrativen Daten.',
    'page-projects-notice': 'Diese Projekte decken drei Kompetenzbereiche ab, die für angewandte Data-Science relevant sind: Analyse öffentlicher Verwaltungsdaten, kausale Politikanalyse und reproduzierbare ML-Ingenieurpraxis. Projektstatusangaben sind explizit und ehrlich: vollständige Analyse, reproduzierbarer Prototyp oder begutachtete Forschungsarbeit.',
    'page-projects-groupA-label': 'A. Angewandtes Data-Science-Portfolio',
    'page-projects-groupA-heading': 'Eigenständige Portfolioprojekte',
    'page-projects-groupA-desc': 'Eigenständig entwickelte Projekte auf öffentlich zugänglichen Daten, die End-to-End-Analyseworkflows demonstrieren: von der Datenquelle bis zum reproduzierbaren Output.',
    'page-projects-groupB-label': 'B. Forschungsbasierte quantitative Analyse',
    'page-projects-groupB-heading': 'Abgeschlossene akademische und Forschungsarbeiten',
    'page-projects-groupB-desc': 'Abgeschlossene Analysen in formalen Forschungs- und akademischen Kontexten, auf realen Datensätzen mit etablierten Methoden der kausalen Inferenz, vollständig begutachtet und benotet.',

    // --- Theses page ---
    'page-theses-hero-title': 'Wissenschaftliche Arbeiten',
    'page-theses-hero-desc': 'Maschinelles Lernen, statistische Modellierung, Kausalinferenz und Datenanalyse: Universität zu Köln und LSE.',
    'page-theses-section-stat': 'Statistische Theorie',
    'page-theses-section-quant': 'Quantitative Politikanalyse',
    'page-theses-section-behav': 'Verhaltenswissenschaft & Messphilosophie',
    'page-theses-section-bsc': 'Bachelorarbeiten, Universität zu Köln',

    // --- Contact page ---
    'page-contact-hero': 'Kontakt',
    'contact-card-title': 'Kontaktdaten',

    // --- Application portfolio ---
    'page-app-hero-title': 'Portfolio für eine Data-Science-Tätigkeit im öffentlichen Sicherheitsumfeld',
    'page-app-hero-desc': 'Diese Seite dokumentiert die Nachweise aus meiner bisherigen Forschungs- und Projekttätigkeit, die für eine analytische Data-Science-Position im öffentlichen Sicherheitsbereich besonders relevant sind. Alle Angaben sind durch abgeschlossene Projekte, begutachtete Arbeiten oder mehrjährige Forschungstätigkeit belegt.',
    'page-app-person-heading': 'Zur Person',
    'page-app-req-heading': 'Anforderungen und Nachweise',
    'page-app-proj-heading': 'Besonders relevante Projekte',
    'page-app-skills-heading': 'Werkzeuge und Methoden',
    'page-app-resp-heading': 'Verantwortungsvoller Umgang mit gesellschaftlich sensiblen Daten',
    'page-app-exp-heading': 'Berufliche Erfahrung in der Datenanalyse',
    'page-app-acad-heading': 'Akademischer Hintergrund',
  },

  en: {
    // Navigation
    'nav-home': 'Home',
    'nav-application': 'Application Portfolio',
    'nav-academic': 'Academic Work',
    'nav-projects': 'Projects',
    'nav-contact': 'Contact',

    // Index hero
    'hero-subtitle': 'Data Scientist | Quantitative Analysis of Societal Data',
    'hero-desc': 'I build reproducible analysis workflows for socially relevant research questions: from data preparation and statistical modelling through machine learning to communicating results to different audiences.',
    'hero-btn-projects': 'View Relevant Projects',
    'hero-btn-cv': 'Download CV',
    'hero-btn-methods': 'Methods & Experience',

    // Profile snapshot
    'profile-heading': 'Profile Summary',
    'profile-subtext': 'Four documented areas of competence, each supported by completed projects, graded academic work, or multi-year research practice.',
    'rfcard1-title': 'Quantitative Modelling',
    'rfcard1-body': 'Causal inference (RDD, DiD, PSM), Bayesian econometrics, panel data, distributional regression, and Monte Carlo simulation, documented in graded theses (grade 1.0) and independent research projects.',
    'rfcard2-title': 'Python, R, Stata & Reproducible Pipelines',
    'rfcard2-body': 'Four years of applied practice with pandas, scikit-learn, matplotlib, tidyverse, and ggplot2, using Git, Makefile, pytest, and fully documented analysis workflows.',
    'rfcard3-title': 'Public Administrative and Policy Data',
    'rfcard3-body': 'Analysis of official federal statistics (BMI/BKA) and parliamentary transcript data, with consistent source documentation, checksum validation, and explicit interpretation limits.',
    'rfcard4-title': 'Audience-Appropriate Communication',
    'rfcard4-body': 'Visualisations, concise result summaries, and reports for researchers, decision-makers, and non-specialist audiences, in academic and institutional contexts.',

    // Selected projects section
    'projects-heading': 'Selected Data Projects',
    'projects-subtext': 'Applied case studies on public administrative data, official security statistics, causal policy analysis, and reproducible machine learning workflows.',

    'proj-pmk-title': 'Politically Motivated Crime: Public Data Analysis Dashboard',
    'proj-pmk-status': 'Complete Analysis',
    'proj-pmk-desc': 'Documented analysis workflow for official PMK aggregate data from BMI/BKA publications (2022–2024): checksum-validated dataset, four reproducible visualisations, complete source documentation, and explicit interpretation limits.',
    'demonstrates-label': 'What this shows:',
    'proj-pmk-demonstrates': 'Source documentation, checksum validation, and factual visualisation of official administrative statistics. Every figure traces back to a specific source.',
    'proj-pmk-btn': 'View Project',

    'proj-bfv-title': 'BfV Constitutional Protection Reports: Public Aggregate Data',
    'proj-bfv-status': 'Validated MVP',
    'proj-bfv-desc': 'Documented analysis workflow for official BfV aggregate statistics from constitutional protection reports 2022–2024: personnel potential by phenomenon area (right-wing extremism: 50,250 in 2024), extremist-motivated offences, 8/8 consistency checks passed, complete source documentation at URL level.',
    'proj-bfv-demonstrates': 'Structured extraction of public security statistics, systematic source documentation at URL level, reproducible pipeline on official BfV aggregate data.',
    'proj-bfv-btn': 'View Project',

    'proj-causal-title': 'Causal Policy Analysis with Quasi-Experimental Methods',
    'proj-causal-status': 'Peer-Reviewed Research',
    'proj-causal-desc': 'Two completed, graded analyses using RDD and DiD: Uruguay\'s PANES programme (approximately 10% causal increase in political support; grade: Distinction 83%) and COVID-19 lockdown and life satisfaction (DiD + PSM, HILDA panel, 215,000 observations).',
    'proj-causal-demonstrates': 'Causal reasoning beyond correlation. Identification strategy, assumption testing, robustness checks, and transparent uncertainty communication for policy-relevant questions.',
    'proj-causal-btn': 'View Project',

    'proj-ml-title': 'Reproducible Machine Learning Pipeline',
    'proj-ml-status': 'Engineering Demonstration',
    'proj-ml-desc': 'End-to-end supervised learning workflow: leak-free sklearn pipelines, model comparison (LR, RF, GBM), cross-validation, 11 automated pytest tests, and reproducible documentation. Random Forest: ROC-AUC 0.900.',
    'proj-ml-demonstrates': 'Clean Python project structure, prevention of data leakage, model validation, automated testing, and reproducible output documentation.',
    'proj-ml-btn': 'View Project',

    'proj-all-btn': 'View All Projects',

    // Tools
    'tools-heading': 'Tools & Methods',

    // Responsible data
    'resp-heading': 'Responsible Handling of Socially Sensitive Data',
    'resp-subtext': 'Analytical soundness requires not only methodological care, but also responsible interpretation, especially for data with societal implications. These principles guide all my work.',

    // Experience
    'exp-heading': 'Professional Experience in Data Analysis',

    // Academic background
    'acad-bg-heading': 'Academic Background',
    'acad-bg-cv-btn': 'Download CV',

    // Academic works (index)
    'acad-works-heading': 'Selected Academic Papers',
    'acad-works-all-btn': 'All Academic Papers',

    // CTA
    'cta-heading': 'Explore My Work',
    'cta-desc': 'Applied data projects with reproducible code and documented pipelines, alongside quantitative research papers on statistical theory, econometrics, and causal inference.',
    'cta-btn-projects': 'View Projects',
    'cta-btn-application': 'Application Portfolio',
    'cta-btn-contact': 'Contact',

    // Footer
    'footer-copyright': '© 2026 Jonathan Gödeke. All rights reserved.',
    'footer-cv': 'Download CV',

    // --- Projects page ---
    'page-projects-hero-title': 'Applied Data Science Projects',
    'page-projects-hero-desc': 'Selected case studies documenting my analytical approach: research question, data preparation, modelling, validation, visualisation, and reproducible workflows on public, institutional, and administrative data.',
    'page-projects-notice': 'These projects cover three competence areas relevant to applied data science: analysis of public administrative data, causal policy analysis, and reproducible ML engineering practice. Project status labels are explicit and honest: complete analysis, reproducible prototype, or peer-reviewed research.',
    'page-projects-groupA-label': 'A. Applied Data Science Portfolio',
    'page-projects-groupA-heading': 'Independent Portfolio Projects',
    'page-projects-groupA-desc': 'Independently developed projects on publicly accessible data, demonstrating end-to-end analysis workflows from data source to reproducible output.',
    'page-projects-groupB-label': 'B. Research-Based Quantitative Analysis',
    'page-projects-groupB-heading': 'Completed Academic and Research Papers',
    'page-projects-groupB-desc': 'Completed analyses in formal research and academic contexts, on real datasets using established causal inference methods, fully graded and reviewed.',

    // --- Theses page ---
    'page-theses-hero-title': 'Academic Work',
    'page-theses-hero-desc': 'Machine learning, statistical modelling, causal inference, and data analysis: University of Cologne and LSE.',
    'page-theses-section-stat': 'Statistical Theory',
    'page-theses-section-quant': 'Quantitative Policy Analysis',
    'page-theses-section-behav': 'Behavioural Science & Philosophy of Measurement',
    'page-theses-section-bsc': 'Bachelor Theses, University of Cologne',

    // --- Contact page ---
    'page-contact-hero': 'Contact',
    'contact-card-title': 'Contact Details',

    // --- Application portfolio ---
    'page-app-hero-title': 'Portfolio for a Data Science Role in the Public Security Sector',
    'page-app-hero-desc': 'This page documents evidence from my research and project work that is particularly relevant for an analytical data science position in the public security sector. All claims are supported by completed projects, graded academic work, or multi-year research practice.',
    'page-app-person-heading': 'About Me',
    'page-app-req-heading': 'Requirements and Evidence',
    'page-app-proj-heading': 'Most Relevant Projects',
    'page-app-skills-heading': 'Tools and Methods',
    'page-app-resp-heading': 'Responsible Handling of Socially Sensitive Data',
    'page-app-exp-heading': 'Professional Experience in Data Analysis',
    'page-app-acad-heading': 'Academic Background',
  }
};
