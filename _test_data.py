from nltk.corpus import stopwords

join_word_list = [('social', 'media'), ('et', 'al'), ('google', 'scholar'), ('big', 'data'), ('web', 'science'),
                  ('science', 'google'),
                  ('crossref', 'google'), ('machine', 'learning'), ('new', 'york'), ('african', 'american'),
                  ('united', 'states'), ('crossref', 'web'),
                  ('data',
                   'collection')]

swap_word_list = [(['bd'], ['big', 'data'])]

stop_word_list = stopwords.words('english')
extended_stop_words = ['from', 'subject', 're', 'edu', 'use']

ignore_word_list = []

test_text = "Introduction Big data (BD) is difficult to define. Precisely the features, scope, purview or threshold" \
            " of BD continues to sow confusions and generate ethical controversies. Despite the preceding, the " \
            "emerging consensus (Ekbia et al. 2015: p. 3; Alharthi et al. 2017: p. 286) is that BD is characterized" \
            " by 5 Vs: Volume (that is, a vast amount of datasets requiring innovative and big tools for capturing, " \
            "storing and analyzing); variety (un/semi/structured and collected from diverse sources);" \
            " velocity (rapidly evolving datasets and expanded by actual data streams); " \
            "veracity (that is, data uncertainty, quality, reliability or predictive force); " \
            "and value (this is the artificial intelligence that is created either for learning new patterns " \
            "in vast datasets or offering personalized services).There is a growing adoption of BD in various " \
            "fields (engineering, life sciences, business, behavioural studies, online and offline commerce, " \
            "education and politics). This article focuses on healthcare big data use and access. Healthcare " \
            "big data (HBD) come from different sources such as sequencing data, Electronic Health Records " \
            "(EHR), biological specimens, Quantified Self (QS), biomedical data, patient-reported data, " \
            "biomarker data, medical imaging, large clinical trials; which may be stored in repositories or " \
            "biobanks (Mittelstadt et al. 2016: p. 306). Other means of expanding HBD streams include healthcare " \
            "literature databases like PubMed, automated sources like health and fitness devices and volunteered " \
            "sources such as e-health networks like patientslikeme.HBD analytics integrates, explores, identifies" \
            " clusters, correlates, analyze and infer (with an unparalleled degree of exactitude) based on datasets" \
            " from the preceding complex heterogeneous sources to create – HBD – value or (artificial) intelligence" \
            " for offering a range of personalized health services, support health policies or clinical decisions," \
            " or advance science (Michael et al. 2013: p. 22). The HDB value relies mostly on analytic techniques" \
            " such as algorithms and machine learning that are generated from processed data. HBD may be " \
            "processed by using graphics processing units or cloud computing. The advancement in the omics " \
            "studies, patient-contributed online data, imaging processes and the increasing affordability and " \
            "accessibility of health electronic devices also imply that a large volume of heterogeneous data can " \
            "now be analyzed to create HBD intelligence at a low cost. Advances have also been made in " \
            "extracting previously difficult text data (from doctor’s notes, millions of books photographs " \
            "from the past) for data analytics and mining purposes.Notwithstanding its (potential) benefits, HBD" \
            " also creates a challenge for all stakeholders such as data utilizers, contributors and " \
            "beneficiaries of HBD intelligence. New digital technologies can empower, yet they are also " \
            "intrusive. HBD vividly exemplifies this dual character (Ekbia et al. 2015: p. 27). As an example, " \
            "digital surveillance can usefully provide support for contact tracing in the event of a virus " \
            "outbreak such as the COVID-19/Ebola outbreak. It could also monitor an individual’s healthcare " \
            "decisions, behaviors or outcomes with the aim of fostering healthy habits and practices in the " \
            "individual or the wider population, providing critical insights on health needs or status, " \
            "assisting with the development of equitable interventions. However, it also introduces a level of " \
            "oversight that significantly threatens individuals’ privacy.Furthermore, HBD may also be abused or " \
            "misused. The literature is awash with examples of data misuse."