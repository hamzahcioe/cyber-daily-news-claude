# Sources

Principles
- Global by design. Every region group below is attempted on every run. A story's importance decides whether it is included, never the region it came from or the language it was published in.
- Primary sources beat reporting about them: national CERTs, regulators, courts, companies' own statements and status pages are listed alongside the media for each region.
- Read non-English sources in the original language and translate. Mark the item's source as "(translated from <language>)". Do not rely on a single machine-translated summary for a contested claim.
- Label state-run and state-aligned media as such and treat their statements as claims: Xinhua, People's Daily, Global Times, CGTN, CCTV, TASS, RIA Novosti, RT, Sputnik, IRNA, Press TV, Tehran Times, Al-Manar, KCNA, SANA, and others you identify. Where the outlet is privately owned but government-aligned, say so in plain words rather than a label.
- Fetch each source directly (front page, tech/security section, feed). For feeds try the site's /feed, /rss, /rss.xml or /atom.xml. When searching, filter by the outlet's own domain and, where the tool allows, the region (user_location), and add the organisation or country name to the query. Do not treat a search result list as coverage of a region.
- If a source fails, try its feed, an alternate section URL, the organisation's own press page, then a targeted search naming the organisation. Record every source that could not be read and why in `sourcesSwept`. If a whole region group fails, say so plainly; never fill the gap with material from another region.
- Balance check before writing: list how many selected items come from each region and each language. If any single country accounts for more than about 40 percent of items, re-check the other regions' groups for stories that were missed or under-read before continuing.

Collection is done by `scripts/fetch_feeds.py` from `feeds.json` (the operational feed list). This file is the reference for the editor and researchers: principles, importance filter, the known-blocked list, and per-region primary sources to look for when researching a story. Groups A to F below are reading lists, not separate agents.

## Known blocked (do not fetch these; they failed in the first run)
Reuters, AP, Bloomberg, BBC, Financial Times, The Economist, The Verge, Ars Technica, Wired, Politico, DW, The Guardian, The Telegraph, The Times, Sky News section pages (use the Sky RSS feed instead), CNA, The Straits Times, The Hindu, Economic Times, Moneycontrol, Heise, Der Spiegel, Süddeutsche, Le Monde, Les Echos, Tweakers, Euractiv, El País, Yonhap, Chosun Biz, NHK feeds, KCNA, Press TV, Tehran Times, Fars, Tasnim, Arab News, Times of Israel, +972, Al Arabiya, Al-Ahram, MSRC blog, Sophos, Positive Technologies, SEC EDGAR HTML pages, Federal Register HTML, Reddit, Downdetector, Uptime Institute, Cloudflare Radar, Techpoint Africa, MyBroadband, Mediapart, Amnesty Security Lab, Lookout, vx-underground, Israel National Cyber Directorate, UAE Cyber Security Council, Roskomnadzor, Russian MoD, SSSCIP, CERT-UA (JS shell).
Wire and paywalled outlets are covered through what does work: Techmeme, Semafor, The Information feed and the syndicated or quoted copies that appear in readable outlets (state this in the item's sources, e.g. "Reuters, as carried by X"). If a feed or section URL is found to work, use it.
Known to work well: RSS feeds of The Register, Computer Weekly, Infosecurity Magazine, BleepingComputer, Dark Reading, SC World, SecurityWeek, Security Affairs, Help Net Security, Cybernews, Schneier, The Record, TechCrunch, CNBC, Al Jazeera (all.xml), France 24, Techmeme (feed.xml), SCMP, TechNode, Pandaily, iThome, Taipei Times, DigiTimes, Meduza, Moscow Times, Kyiv Independent (category page), Ukrinform, TASS and RIA RSS, Middle East Eye, Al-Monitor, Haaretz and Jerusalem Post homepages, TechCabal /feed/, ITWeb, Rest of World, CISA KEV JSON, NVD API 2.0, php.net, openssl.org, Google Cloud and Cloudflare status feeds.

## Group A: cyber-and-vulns

### cyber-core
Reporting and research on security, from several regions.
- Risky Business (Australia/global): https://risky.biz/newsletters/ , Risky Bulletin and Seriously Risky Business; fetch the index, then issue pages and the primary links in them
- Report URI blog (UK): https://blog.report-uri.com/ (feed https://blog.report-uri.com/rss/)
- SecurityWeek, The Citizen Lab (https://citizenlab.ca/), Schneier on Security, Krebs on Security, The Record
- The Register (UK), Computer Weekly (UK), Infosecurity Magazine (UK), The Hacker News, BleepingComputer, Dark Reading, SC World, CyberInsider, Security Affairs (Italy), Help Net Security, Cybernews, The Cyber Express
- Researchers and vendors: Microsoft Security Blog and MSRC, Google Threat Intelligence and Project Zero, Kaspersky Securelist (Russia/global), ESET WeLiveSecurity (Slovakia), Cisco Talos, Palo Alto Unit 42, Check Point Research (Israel), Trend Micro Research (Japan), Sophos, Bitdefender, Positive Technologies (Russia), Qi An Xin and 360 Threat Intelligence (China), Group-IB, Recorded Future, Mandiant, Horizon3.ai, Malwarebytes, HackerOne, Okta security, AWS security bulletins
- Where a vendor is state-adjacent or has a national interest, say so in the item.

### status-vulns-supply-chain
CISA KEV and advisories; NVD, OSV, GitHub advisories, EUVD; php.net, openssl.org and other maintainer security pages; Microsoft 365 and Azure service health, Apple System Status, Google Cloud and Workspace status, AWS Health, Cloudflare status; PyPI, npm, GitHub, VS Code extensions; Socket, Wiz, Snyk, Aikido; Reddit r/cybersecurity and r/netsec, Hacker News front page. Fallbacks for status pages: the provider's status feed or JSON endpoint, then the incident history page.

## Group B: leaks-and-investigations

### investigative-leaks
Often ahead of mainstream outlets; treat everything here as claims until verified.
Distributed Denial of Secrets, WikiLeaks, Forbidden Stories, OCCRP, ICIJ, Lighthouse Reports, Bellingcat, The Intercept, 404 Media, Follow the Money (Netherlands), Correctiv (Germany), Disclose (France), Mediapart (France), Süddeutsche Zeitung investigations, Meduza and Novaya Gazeta Europe investigations, The Insider (Russia), Kyiv Independent investigations, Haaretz, +972 Magazine, Middle East Eye, Calcalist, The Citizen Lab, Amnesty Security Lab, Access Now, Privacy International, EFF, Lookout, Google TAG, DataBreaches.net, Have I Been Pwned recent breaches, ransomware.live, ransomlook.io, and researcher chatter via HackManac, FalconFeeds, vx-underground, Dark Web Informer.

## Group C: uk-and-europe

### uk
Media: BBC Technology, Sky News Tech, The Guardian technology, Financial Times, The Telegraph technology, The Times technology, Computing, The Stack, UKAuthority, Public Technology, Civil Service World, Third Sector, Charity Digital, Computer Weekly, The Register, Infosecurity Magazine.
Primary: NCSC (ncsc.gov.uk), ICO (ico.org.uk), gov.uk announcements on cyber, data protection and digital, National Crime Agency, Action Fraud, Cyber Essentials/IASME, Charity Commission, Ofcom, FCA, Bank of England, Border Force/HMRC/CDS, Parliament committees, UK Finance, major UK banks' and telecoms' status pages, Downdetector UK.
Fallbacks: site feeds, gov.uk search and content API pages for the organisation, the organisation's press page. If UK sources fail, say so plainly in `sourcesSwept` and the UK section.

### europe
Media: Heise and Golem (Germany), Netzpolitik (Germany), Der Spiegel and Süddeutsche (tech/digital), Le Monde (Pixels), Next.ink (France), Les Echos (tech), Tweakers (Netherlands), NOS (tech), Euractiv, Politico Europe, Euronews, DW, France 24, El País Tecnología, Xataka (Spain), Red Hot Cyber (Italy), Il Sole 24 Ore (tech), Niebezpiecznik (Poland), Computer Sweden, Digi.no (Norway), Yle (Finland).
Primary: ENISA, CERT-EU, Europol, Eurojust, EDPB, ANSSI and CERT-FR, CNIL, BSI (Germany), NCSC-NL and Autoriteit Persoonsgegevens, CERT Polska, NCSC Finland, AGID/ACN (Italy), INCIBE (Spain), EU Official Journal for legislation.

## Group D: americas-wires-ai-markets

### americas
Media: Reuters, AP, Bloomberg, Axios, The Verge, Ars Technica, TechCrunch, Wired, CNBC tech, The Globe and Mail and CBC (Canada), Rest of World, Infobae tecnología (Argentina), Folha de S.Paulo tec and Tecnoblog (Brazil), Convergência Digital (Brazil), Xataka México, El Universal tecnología (Mexico), El Mercurio and Emol (Chile).
Primary: CISA (advisories and KEV), FBI/IC3, DOJ (justice.gov), SEC EDGAR (8-K cyber disclosures), FTC, FCC, Treasury/OFAC, US court dockets via CourtListener, Canadian Centre for Cyber Security, CERT.br, national data-protection authorities (ANPD Brazil, INAI Mexico).

### global-wires-and-tech
Reuters, AP, AFP, Bloomberg, BBC, Al Jazeera, DW, France 24, NHK World, CNA, Financial Times, The Economist, Techmeme, The Information, Rest of World, Semafor.

### ai-and-industry
Labs and companies (official announcements, release notes, papers): OpenAI, Anthropic, Google DeepMind, Meta AI, Microsoft AI, Mistral, Alibaba Qwen, Tencent Hunyuan, ByteDance Seed, DeepSeek, Moonshot, Zhipu, Baidu, SenseTime, Samsung, Naver, Sakana, Sarvam, Cohere, xAI. Industry: arxiv.org when a story points to a paper, Hugging Face blog, SemiAnalysis, TrendForce, DigiTimes, SEMI, SIA, Epoch AI. Regulators and standards: EU AI Office, UK AISI, US NIST/CAISI, China CAC, Japan AI Strategy HQ, Korea MSIT.

### markets-and-events
SEC EDGAR, HKEX, SGX, Tokyo Stock Exchange, NASDAQ and NYSE notices, company investor-relations pages, publisher and developer announcements (game and product launches), conference and summit programmes (APEC, G7/G20 digital tracks, Mobile World Congress, Black Hat/DEF CON, CES), court and regulator calendars.

## Group E: asia-pacific

### east-asia
Media (China, HK, Taiwan): SCMP tech, Caixin Global, 36Kr, TechNode, Pandaily, Jiemian, The Paper, Sina/Tencent/NetEase tech, Taiwan Focus Taiwan, Taipei Times, DigiTimes, iThome (Taiwan).
Media (Japan, Korea): Nikkei Asia, NHK World, Japan Times, ITmedia, Nikkei xTECH, Korea Herald, Korea JoongAng Daily, Yonhap, ZDNet Korea, Chosun Biz.
State media (label): Xinhua, People's Daily, Global Times, CGTN, CCTV, China Daily, KCNA.
Primary: CNCERT/CC and MIIT/CAC announcements (China, labelled as government claims), TWCERT/CC, JPCERT/CC and NISC (Japan), KISA and KrCERT (Korea), HKCERT.

### south-southeast-asia-oceania
Media: The Hindu, The Economic Times tech, MediaNama, The Print, Moneycontrol tech, Dawn (Pakistan), The Daily Star (Bangladesh), Channel NewsAsia, The Straits Times, Tech in Asia, KrASIA, e27, DealStreetAsia, The Jakarta Post, Rappler, VnExpress, ABC News (Australia), iTnews, The Guardian Australia, The Register APAC, RNZ and Stuff (New Zealand).
Primary: CERT-In (India), Cyber Security Agency of Singapore, ACSC (cyber.gov.au), CERT NZ/NCSC NZ, OAIC, Pakistan PTA, Indonesia BSSN, Vietnam VNCERT.

## Group F: russia-ukraine-middle-east-africa-infrastructure

### russia-ukraine-eastern-europe
Independent/exile media: Meduza, The Moscow Times, Novaya Gazeta Europe, The Insider, Kyiv Independent, Ukrainska Pravda, Ukrinform (state news agency, label), Mediazona, RFE/RL, Belsat, Notes from Poland, Euractiv, Balkan Insight.
Russian state and state-aligned (label): TASS, RIA Novosti, RT, Sputnik, Izvestia, Kommersant (privately owned, treat with care), Interfax.
Primary: CERT-UA and SSSCIP (Ukraine, government claims), Ukrainian General Staff and Ministry of Defence, Russian ministries (claims), Roskomnadzor, Polish CERT, Baltic NCSCs.

### middle-east-north-africa
Media: Al Jazeera, Al-Monitor, Middle East Eye, The National (UAE), Arab News, Gulf News, Haaretz, Times of Israel, +972 Magazine, Calcalist/CTech, Jerusalem Post, Iran International (opposition-aligned, label), Hürriyet Daily News and Duvar English (Turkey), Daily Sabah (government-aligned, label), Al-Ahram and Mada Masr (Egypt), Al Arabiya (Saudi-backed, label).
State and state-aligned (label): IRNA, Press TV, Tehran Times, Fars, Tasnim, SANA, Al-Manar, WAM, SPA, QNA.
Primary: Israel National Cyber Directorate, UAE Cyber Security Council, Saudi NCA, Iranian officials' statements (claims).

### africa
Media: TechCabal (Nigeria), Techpoint Africa, Disrupt Africa, Rest of World, ITWeb and MyBroadband (South Africa), The Continent, Daily Maverick, Business Daily (Kenya), The EastAfrican, Ahram Online, Jeune Afrique, Agence Ecofin (digital).
Primary: national CERTs and data regulators (Nigeria NDPC, South Africa Information Regulator, Kenya ODPC, Egypt, Morocco DGSSI), Africa Cybersecurity resource pages where updated.

### infrastructure-and-physical
Reuters, AP, Al Jazeera, Kyiv Independent, Ukrinform, official ministry statements (claims), Data Center Dynamics, Uptime Institute, Submarine Telecoms Forum, TeleGeography, Submarine Networks, NetBlocks, Cloudflare Radar, Kentik, RIPE and APNIC labs, ENTSO-E, Ofgem, Ukrenergo.

## Importance filter
A) Cyber and infrastructure: major vendor and platform incidents and outages; critical or actively exploited vulnerabilities and security releases in widely deployed software; active campaigns (nation-state, ransomware, DDoS, hacktivism, mass phishing, infostealers); supply-chain compromises with wide blast radius; ransomware claims and leak-site postings on major names and notable leaks; law enforcement and policy; UK items given equal weight to everything else.
B) Global tech (MAJOR ONLY, except significant leak, investigative and research findings): geopolitics and tech (export controls, summits, semiconductors, robotics); AI developments worldwide; physical and infrastructure attacks (strikes on data centres, telecom and power, cable cuts); state spying and surveillance; major tech news (IPOs, flagship launches, top executive changes, acquisitions, antitrust).
C) World and economy (major only): breaking international news (wars and strikes including attacks on airports, ports, power and telecoms; coups, elections, summits, sanctions, diplomacy with wide effect); economy and trade with wide reach (central banks, tariffs, major data, market shocks); China and Asian technology (AI models and chips, EVs, batteries, solar and new-energy developments); energy and climate-tech milestones. State media (Xinhua, CGTN, Global Times, China Daily, TASS, RIA, Anadolu) is labelled as such and its statements are claims.
D) Science and research (top items only): major discoveries and results from Nature, Science, New Scientist, Quanta, Ars Technica Science, Phys.org and agency feeds (ESA, NASA); preprints are flagged as such; press releases are claims. Research and innovation policy in the US, UK and Europe: government strategies and budgets, funding calls, research regulation (UKRI, DSIT, CORDIS, Science|Business, Times Higher Education, AIP FYI).
E) Travel and nature (a few, high quality only): National Geographic, Smithsonian Magazine, Atlas Obscura, Mongabay, Yale E360 and similar; no promotional or deal content.
Skip routine patch-cycle noise unless critical or exploited, small breaches with no wider relevance, opinion, vendor marketing.
