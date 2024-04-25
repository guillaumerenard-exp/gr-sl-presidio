import pandas
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
import streamlit as st

# App title
st.set_page_config(page_title="Presidio MC")
st.title("Presidio MC")

language = st.selectbox(label="Select a language", options=["en", "fr"], index=1)
source_text = st.text_area("Enter your text here: ", height=200, max_chars=5000)

if source_text != "":
    st.header("Source text")
    with st.expander("See source text"):
        st.write(source_text)

    with st.spinner('Anonymizing text...'):
        # Initialize the engine:
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {"lang_code": "en", "model_name": "en_core_web_lg"},
                {"lang_code": "fr", "model_name": "fr_core_news_md"}
            ],
        }

        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine_with_french = provider.create_engine()

        analyzer = AnalyzerEngine(nlp_engine=nlp_engine_with_french, supported_languages=["en", "fr"])
        analyze_results = analyzer.analyze(text=source_text, language=language)
        analyze_results_df = pandas.DataFrame.from_records([result.to_dict() for result in analyze_results], exclude=["recognition_metadata"])
        
        st.header("Entities")
        st.table(data=analyze_results_df)

        # Initialize the engine:
        anonymizer_engine = AnonymizerEngine()
        anonymized_result = anonymizer_engine.anonymize(text=source_text, analyzer_results=analyze_results)

        st.header("Anonymized text")
        st.write(anonymized_result.text)