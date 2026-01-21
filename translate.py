import streamlit as st
from huggingface_hub import InferenceClient



# ------------------------------------------------------------
# prompt templates
# ------------------------------------------------------------
def get_translation_prompt(text):
    """
    Returns a translation prompt for a given text.
    """
    return (f"translate: {text}")


def get_sentiment_analysis_prompt(text):
    """
    Returns a prompt asking the model to classify sentiment.
    """
    return f"analyze sentiment: {text}"

# ------------------------------------------------------------
# model integration
# ------------------------------------------------------------
from datetime import datetime


def get_state():
    return st.session_state

def chat_with_model(prompt, container, tab):
    """
    Send a chat request to Watson X and display the response.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model_id: The model identifier to use
        container: Streamlit container for displaying response
        
    Returns:
        str: The response text, or None if error
    """
    state = get_state()
    model_id = state.model_id
    client = state.client
    params = state.params
    source_lang = state.source_lang
    target_lang = state.target_lang
    user_api_key = state.user_api_key
    #print("prompt: ", prompt)
    print("source_lang: ", source_lang)
    #print("target_lang: ", target_lang)
    print("model_id: ", model_id)
    
    try:
        response_placeholder = container.empty()
        response_placeholder.info("🔄 Processing request...")

        # Hugging Face T5 call
        current_datetime = datetime.now().time().strftime("%H:%M:%S")

        ret_messages = {"task": {"translation": None, "sentiment": None}}
        
        if tab == 1: # Translation
            # Translation model selection
            if source_lang == "eng_Latn":
                st.session_state.model_id = st.session_state.model_id_en_fr
                result = client.translation(
                        prompt,
                        model=st.session_state.model_id_en_fr,
                        src_lang=source_lang,
                        tgt_lang=target_lang
                    )
                translation_result = result.translation_text
                split_trans = translation_result.split()[2:]
                joined_trans = " ".join(split_trans)
                # response_placeholder.markdown(" ".join(split_trans))
                # print(
                #   "result:", 
                #   {"translation": translation,
                #    "split_trans" translation.split(),
                #   .join(split_trans), 
                #    "time": current_datetime}
                # )
                ret_messages['task']['translation'] = joined_trans

            elif source_lang == "fra_Latn":
                st.session_state.model_id = st.session_state.model_id_fr_en
                result = client.translation(
                        prompt,
                        model=st.session_state.model_id_fr_en,
                        src_lang=source_lang,
                        tgt_lang=target_lang
                    )
                translation_result = result.translation_text
                split_trans = translation_result.split()[1:]
                joined_trans = " ".join(split_trans)
                #response_placeholder.markdown(" ".join(split_trans))
                # print(
                #   "result:", 
                #   {"translation": translation,
                #    "split_trans" translation.split(),
                #   .join(split_trans), 
                #    "time": current_datetime}
                # )
                ret_messages['task']['translation'] = joined_trans
                response_format = f"""
                                Translation: {ret_messages['task']['translation']}
                               """
                response_placeholder.markdown(response_format)

        elif tab == 2: # Sentiment Analysis
            # Sentiment analysis model selection
            sentiment = client.text_classification(
                prompt,
                model=st.session_state.model_id_sentiment_analysis,
            )
            # print("sentiment: ", sentiment[0])
            
            sentiment_by_score = (sentiment[0]['label'], sentiment[0]['score'])
            # print("sentiment: ", sentiment_by_score)

            ret_messages['task']["sentiment"] = sentiment_by_score

            response_format = f"""
                                Sentiment: {ret_messages['task']['sentiment'][0]}\n\n
                                Score: {ret_messages['task']['sentiment'][1]}
                               """
            response_placeholder.markdown(response_format)

        return ret_messages

    except Exception as e:
        container.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def stream_response(prompt, container, tab):
    """
    Main entry point for streaming responses.
    Routes to Watson X chat.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        container: Streamlit container for displaying response
        model_name: Model identifier from dropdown
        
    Returns:
        str: Response text or None
    """
    
    return chat_with_model(prompt, container, tab)




def setup_page():
    """
    Sets up the page with custom styles and page configuration.
    """
    st.set_page_config(
        page_title="Advanced Translator",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        :root {
            --llama-color: #4e8cff;
            --llama-color-light: #e6f0ff;
            --llama-color-dark: #1a3a6c;
            --llama-gradient-start: #4e54c8;
            --llama-gradient-end: #8f94fb;
        }
        .stApp {
            margin: auto;
            background-color: var(--background-color);
            color: var(--text-color);
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .logo-container img {
            width: 150px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def user_key_handler(user_api_key):
    if user_api_key:
        st.session_state.user_api_key = user_api_key
        client = get_client(st.session_state.user_api_key)
        return client
    else:
        st.error("No key provided. Please paste your API key.")
        
def get_client(user_api_key):
    if user_api_key:
        client = InferenceClient(
            provider="hf-inference",
            api_key=user_api_key,
        )
        if client:
            st.success("Key saved successfully")
            st.session_state.client = client
            return client
        else:
            st.error("Invalid credentials. Please try again.")
            return None
    else:
        st.error("No key provided. Please paste your API key.")
        return None

def key_handler(user_api_key):
    client = get_client(st.session_state.user_api_key)
    st.session_state.client = client
    return client

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    setup_page()

    # Header section with title and subtitle
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 class="header-title">🦙 Translator</h1>
            <p class="header-subtitle">Hugging Face models</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Meta logo
    st.markdown(
        """
        <div class="logo-container">
            <img src="https://www.translatedright.com/wp-content/uploads/2021/10/why-you-shouldnt-use-google-translate-for-business-1-scaled-2560x1280.jpg" alt="Translation Logo">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Remove the Llama image display

    # Sidebar for settings
    with st.sidebar:
        st.title("🦙 Settings")
        
        user_api_key = st.sidebar.text_area(
            "Hugging FaceAPI Key:",
            height=150,
            width="stretch",
            key="user_api_key"
        )
    
        # returns client object
        key_clicked_client = st.sidebar.button(
            "Save Key",
            on_click=lambda: key_handler(user_api_key),
            key="save_key_btn"
        )
    
        langs = ["eng_Latn", "fra_Latn"]

        source_lang = st.selectbox(
            "From", langs
        )
        st.session_state.source_lang = source_lang

        target_lang = st.selectbox(
            "To", [lang for lang in langs if lang != st.session_state.source_lang]
        )
        st.session_state.target_lang = target_lang

        cultural_context = st.selectbox(
            "Context", ["Formal", "Casual", "Business", "Youth Slang", "Poetic"]
        )
        st.session_state.cultural_context = cultural_context

    # Main container with border
    main_container = st.container(border=True)

    # sidebar results output
    session_results = {"session": None, "results": None, "score": None}

    with main_container:
        st.header("Enter Text for Translation and Analysis")
        text = st.text_area(
            "Text to translate",
            "L'affaire des poisons tourne au cauchemar politique...",
            height=200,
        )
        st.caption(f"Character count: {len(text)}")
        st.session_state.messages = text

        if st.button("Translate and Analyze", type="primary", key="translate_and_analyze_btn"):
            if text and st.session_state.client:
                # Tabs for different analysis types
                tab1, tab2 = st.tabs(
                    [
                        "Translation",
                        "Sentiment Analysis"
                    ]
                )
               
                # Tab 1: Translation
                with tab1:
                    st.subheader("Result")
                    translation_container = st.empty()
                    translation_prompt = get_translation_prompt(st.session_state.messages)
                    st.session_state.translation_prompt = translation_prompt
                    #print("translation_prompt: ", translation_prompt)
                    
                    try:
                        translation = stream_response(
                            translation_prompt,
                            translation_container,
                            1
                        )      
                                     

                    except Exception as e:
                        print("ret_trans_except: ", e)
                
                #Tab 2: Sentiment Analysis
                with tab2:
                    st.subheader("Result")
                    sentiment_container = st.empty()
                    sentiment_prompt = get_sentiment_analysis_prompt(st.session_state.messages)
                    st.session_state.sentiment_prompt = sentiment_prompt
                    #print("sentiment_prompt: ", sentiment_prompt)
                    
                    try:
                        sentiment = stream_response(
                            sentiment_prompt,
                            sentiment_container,
                            2
                        )         
                                
                    except Exception as e:
                        print("ret_sentiment_except: ", e)
            else:
                st.error("Please enter key!")
                
    # Sidebar for additional information and feedback
    with st.sidebar:
        st.subheader("About")
        st.info("Demo app - Hugging Face models")


def init_state():
    defaults = {
        "key_clicked": False,
        "user_api_key": None,
        "model_id": None,
        "model_id_en_fr": "Helsinki-NLP/opus-mt-tc-big-en-fr",
        "model_id_fr_en": "Helsinki-NLP/opus-mt-fr-en",
        "model_id_sentiment_analysis": "tabularisai/multilingual-sentiment-analysis",
        "client": None,
        "result": None,
        "params": {
            "src_lang": "en",
            "tgt_lang": "fr",
            "clean_up_tokenization_spaces": True,
            "truncation": "do_not_truncate",
            "generate_parameters": {
                "temperature": 0.5,
            }
        },
        "messages": None,
        "translation_prompt": None,
        "source_lang": "en",
        "target_lang": "fr",
        "cultural_context": "formal",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ------------------------------------------------------------
# Run App
# ------------------------------------------------------------
if __name__ == "__main__":
    init_state()
    main()
    