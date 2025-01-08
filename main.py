import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_llm

st.title("AI Web Scrapper")
url = st.text_input("Enter a website URL")

if st.button("Scrape Site"):
    st.write("Scraping website")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    st.session_state.dom_content = cleaned_content
    print(result)
    st.write("Scraping complete")
    with st.expander("View scraped content"):
        st.text_area("Scraped content", value=cleaned_content, height=800)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_llm(dom_chunks, parse_description)
            st.write(parsed_result)