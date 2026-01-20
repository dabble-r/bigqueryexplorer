import streamlit as st
import time
from datetime import datetime


def get_state():
    return st.session_state

def chat_with_model(prompt, container):
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
    hf_token = state.HF_TOKEN
    print("prompt: ", prompt)
    print("source_lang: ", source_lang)
    print("target_lang: ", target_lang)
    
    
    try:
        response_placeholder = container.empty()
        response_placeholder.info("🔄 Processing request...")

        # Hugging Face T5 call
        

        current_datetime = datetime.now().time().strftime("%H:%M:%S")

        if source_lang == "eng_Latn":
            result = client.translation(
                    prompt,
                    model="Helsinki-NLP/opus-mt-tc-big-en-fr",
                    src_lang=source_lang,
                    tgt_lang=target_lang
                )
        elif source_lang == "fra_Latn":
            result = client.translation(
                    prompt,
                    model="Helsinki-NLP/opus-mt-fr-en",
                    src_lang=source_lang,
                    tgt_lang=target_lang
                )

        translation = result.translation_text.split()
        response_placeholder.markdown(" ".join(translation[1:]))
        print("result:", {"translation": translation, "time": current_datetime})
       

        return translation

    except Exception as e:
        container.error(f"Error: {e}")
        return None

    # unreachable
    except Exception as e:
        error_msg = f"Error: {e}"
        container.error(error_msg)
        print(f"Model error: {e}")
        import traceback
        traceback.print_exc()
        return None


def stream_response(prompt, container):
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
    
    return chat_with_model(prompt, container)
