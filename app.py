import streamlit as st

from components.loader import load_youtube_transcript
from components.chunking import create_chunks
from components.embeddings import create_vectorstore
from components.retriever import get_retriever
from components.chain import get_rag_chain


# 🔹 Extract video ID
def extract_video_id(url: str):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url


# 🔹 Cache vectorstore
@st.cache_resource
def build_vectorstore(video_id):
    entries = load_youtube_transcript(video_id)

    if not entries:
        return None

    chunks = create_chunks(entries)
    vectorstore = create_vectorstore(chunks)

    return vectorstore


# 🔹 Page config
st.set_page_config(page_title="YouTube RAG Chatbot")

st.title("🎥 YouTube Chatbot")
st.write("Ask questions about any YouTube video")


# 🔹 Form UI
with st.form("query_form"):
    video_url = st.text_input("Enter YouTube URL")
    query = st.text_input("Ask a question about the video")
    submit = st.form_submit_button("Get Answer")


# 🔹 Show video preview
if video_url:
    st.video(video_url)


# 🔹 Main logic
if submit:
    if not video_url or not query:
        st.warning("Please enter both URL and question")
    else:
        try:
            video_id = extract_video_id(video_url)

            with st.spinner("Processing video and generating answer..."):
                
                # 🔹 Cached vectorstore
                vectorstore = build_vectorstore(video_id)

                if vectorstore is None:
                    st.error("Could not load transcript. Try another video.")
                    st.stop()

                # 🔹 Retriever
                retriever = get_retriever(vectorstore)

                # 🔹 Retrieve chunks
                results = retriever.invoke(query)

                # 🔹 Build context
                context = "\n\n".join([
                    f"[{doc.metadata['start']} - {doc.metadata['end']}]\n{doc.page_content}"
                    for doc in results
                ])

                # 🔹 LLM
                chain = get_rag_chain()

                response = chain.invoke({
                    "context": context,
                    "question": query
                })

            # 🔹 Output
            st.markdown("### 📌 Answer")
            st.markdown(response.content)

            # 🔹 Show timestamps
            st.markdown("### ⏱ Relevant Segments")

            for doc in results:
                start = int(doc.metadata["start"])

                minutes = start // 60
                seconds = start % 60

                timestamp_link = f"{video_url}&t={start}s"

                st.markdown(f"- [{minutes}:{seconds:02d}]({timestamp_link})")

        except Exception as e:
            st.error(f"Error: {str(e)}")