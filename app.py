#######################################################################################################################################################################
####################################################################  Importing Packages ##############################################################################
#######################################################################################################################################################################

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_mic_recorder import mic_recorder
from streamlit_extras.stylable_container import stylable_container
from pydub import AudioSegment
import tempfile
import os
from Functions import *
#docx
from docx import Document
from io import BytesIO

#######################################################################################################################################################################
####################################################################  Page Configuration ##############################################################################
#######################################################################################################################################################################

st.set_page_config(
        page_title="Transcription App",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

#######################################################################################################################################################################
#################################################################  Side Bar Menu Creation  ############################################################################
#######################################################################################################################################################################

with st.sidebar:
    choose = option_menu(menu_title="App Menu",
                         options=["Welcome","User's Manual","App"],
                         icons=['house','gear-wide'],
                         menu_icon="menu-up",
                         default_index=0,
                            #  styles={
                            #         "container": {"padding": "5!important", "background-color": "#fafafa"},
                            #         "icon": {"color": "orange", "font-size": "30px"}, 
                            #         "nav-link": {"font-size": "20px", "text-align": "left", "margin":"5px", "--hover-color": "#eee"},
                            #         "nav-link-selected": {"background-color": "#02ab21"},
                            #       }
                            )
    st.sidebar.markdown('''                                      
    ---
    Created by [CmtProoptiki](https://cmtprooptiki.gr/)
                            ''')

if choose=="Welcome":
    st.title("Welcome to our Transcription App 👋")
    st.write("")
    st.markdown(
      """
    We are thrilled to have you here!

    This application is designed to help you easily convert your audio files into text and provide a concise summary of the content.

    Whether you have recordings of meetings, lectures, interviews, or any other audio, our app will transcribe and summarize them for you.

    🦾Leverage the technology of today to effortlessly transcribe and summarize your audio files with our user-friendly app.

    ### What You Can Do with This App:

    - **Upload Audio Files**: Simply upload your audio files in the supported formats.
    - **Get Transcriptions**: Receive accurate text transcriptions of your audio content.
    - **Summarize Content**: Obtain a brief and meaningful summary of the transcribed text.

    👈**Navigate through the app using the sidebar to explore these features**.
    We hope this tool enhances your productivity and makes managing audio content more convenient for you.

    ### Need more Help?

    Please contact with our [Support Team](https://cmtprooptiki.gr/?page_id=20)
    
    ### See more of our work:

    - Explore [Cmt Prooptiki](https://cmtprooptiki.gr/)
"""  
    )

elif choose== "User's Manual":
    st.title("How to Use 🛠️")
    st.markdown("""
    ### Step-by-Step Guide:
    
    1. **Provide Context**: Provide a brief description of the context or content of the audio. This will help our algorithms generate more accurate transcriptions and summaries tailored to your needs.
                
    2. **Select Number of Speakers (if applicable)**: If your audio file includes multiple speakers, specify the number of speakers present.This information helps improve the accuracy of the transcription and enables the summarization process to distinguish between different speakers.
    3. **Upload Your Audio File**: Choose the Audio File you want to transcribe by clicking on the "Browse files" button.
    4. **View Results and Download**: Once the transcription and summarization processes are complete, you can view the results directly on the app interface. Additionally, you have the option to download the transcribed text and summary for further analysis or reference.
                
    ### Tips:
    - **Provide Accurate Context**: Offer a concise and accurate description of the content or context of the audio file before uploading it. This helps the app's algorithms better understand the content and generate more relevant results.
                            
    - **Provide Clear Audio**: Ensure that the audio files you upload are clear and free from background noise or disturbances. Clear audio improves the accuracy of transcription and summarization.
    - **Review and Edit**: After receiving the transcribed text and summary, take some time to review and edit them if necessary. While the app strives for accuracy, manual review can help correct any errors or inaccuracies.
                
    """)


elif choose== "App":

    #######################################################################################################################################################################
    #############################################################  Audio file Description Input  ##########################################################################
    #######################################################################################################################################################################
    st.subheader("1.Provide the Context of your Audio File:")
    desc=st.text_input(
        label="",
        label_visibility="collapsed",
        max_chars=200,
        help="Give a short description of your audio and press Enter",
        placeholder="The audio file is about..."
    )
    if desc:
        st.write(f"The audio file is about {desc}")
    else:
        st.write("The audio file is about...")
    st.write("")

    #######################################################################################################################################################################
    #############################################################  Number of Speakers Input  ##############################################################################
    #######################################################################################################################################################################

    st.subheader("2.Select the Number of Speakers on your Audio File:")
    speakers=st.slider(
        label="",
        label_visibility="collapsed",
        min_value=1,
        max_value=10, #We could talk about to set this limit
        value=1
    )

    if speakers:
        st.write(f"The number of Speakers are: {speakers}")
    else:
        st.write("The number of Speakers are: ...")
    st.write("")

    #######################################################################################################################################################################
    ###############################################################  Upload the Audio file  ###############################################################################
    #######################################################################################################################################################################
    
    st.subheader("3.Upload Your Audio File:")
    st.write("")
    on=st.toggle("Record the Audio File Live on the App")

    #####################################################################################################################################################################
    ####################################################################  Live Recording File  ##########################################################################
    #####################################################################################################################################################################
    if on:
        audio=mic_recorder(
            start_prompt="Start recording",
            stop_prompt="Stop recording",
            just_once=False,
            use_container_width=False,
            format="wav",
            callback=None,
            args=(),
            kwargs={},
            key=None
            )
        if audio:
            st.audio(audio["bytes"])
            #st.write(audio)
            #Create a temporary file to save the uploaded file
            audio_bytes = audio["bytes"] 
            with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as temp_file:
             temp_file.write(audio_bytes)
             temp_file_path = temp_file.name
            #st.write(f"Temporary file path: {temp_file_path}")
            st.success("Your recording has been saved!")
            transcribe=st.button("Transcribe",type="primary")
            if transcribe:
                with st.spinner("Transcription in progress. Please wait..."):
    #######################################################################################################################################################################
    #########################################################  Load the Audio file and Divide it into Segments  ###########################################################
    #######################################################################################################################################################################
                    # Load your audio file
                    audio = AudioSegment.from_file(temp_file_path)

                    # Define the duration of each segment in milliseconds (e.g., 5 minutes)
                    segment_duration = 5 * 60 * 1000

                    # Split the audio file into segments
                    segments = [audio[i:i + segment_duration] for i in range(0, len(audio), segment_duration)]

                    # Save each segment as a separate file
                    segment_paths = []
                    for idx, segment in enumerate(segments):
                        segment_path = f"{temp_file_path}_segment_{idx}.mp3"
                        segment.export(segment_path, format="mp3")
                        segment_paths.append(segment_path)

                    # # Display the paths of the saved segments
                    # st.write("Segments saved at:")
                    # for path in segment_paths:
                    #     st.write(path)

    #######################################################################################################################################################################
    #########################################################  Initial Transcription using "Whisper-1" model  #############################################################
    #######################################################################################################################################################################
                    # Transcribe each segment
                    transcriptions = [transcribe_segment(path) for path in segment_paths]

                    # Combine all transcriptions into a single transcript
                    full_transcription = " ".join(transcriptions)
                    # st.write(full_transcription)

    #######################################################################################################################################################################
    ######################################################  Improving Reliability using Post-processing with GPT-4 model  #################################################
    #######################################################################################################################################################################
                    # Correct each transcription
                    corrected_transcriptions = [correct_transcription(transcription,desc,speakers) for transcription in transcriptions]

                    # Combine all corrected transcriptions into a single transcript
                    full_corrected_transcription = " ".join(corrected_transcriptions)
                    #st.write(full_corrected_transcription)

    #######################################################################################################################################################################
    ######################################################  Improving Reliability using Post-processing with GPT-4 model  #################################################
    #######################################################################################################################################################################

                    summary=summarize_transcription(full_corrected_transcription)
                    #st.write(summary)

    #######################################################################################################################################################################
    ############################################################################  Results  ################################################################################
    #######################################################################################################################################################################
            
                #Show the Results directly on the app's interface
                st.subheader("4.Results:")
                st.write("")
                st.subheader("Summary:")
                st.write(summary)
                st.subheader("Full Transcription:")
                st.write(full_corrected_transcription)
                
                #Docx Creation Function:
                buffer=docx_creation(summary,full_corrected_transcription)

                #Download button
                st.download_button(
                    label="Download Results",
                    data=buffer,
                    file_name="Transcription Results.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            







    ####################################################################################################################################################################        
    ####################################################################  Already Recorded File  #######################################################################   
    ####################################################################################################################################################################
    else:
        file=st.file_uploader(
            label="test1",
            label_visibility="collapsed",
            type=["mp3","mp4","wav"],
            accept_multiple_files=False,
            help="HEEEEELP",
            key=1
            )
        if file:
            st.audio(file)
            #st.write(file.name)
            # Create a temporary file to save the uploaded file
            with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name
            #st.write(f"Temporary file path: {temp_file_path}")
            st.success("Your file has been Uploaded!")
            transcribe=st.button("Transcribe",type="primary")

            if transcribe:
                with st.spinner("Transcription in progress. Please wait..."):
    #######################################################################################################################################################################
    #########################################################  Load the Audio file and Divide it into Segments  ###########################################################
    #######################################################################################################################################################################

                    # Load your audio file
                    audio = AudioSegment.from_file(temp_file_path)

                    # Define the duration of each segment in milliseconds (e.g., 5 minutes)
                    segment_duration = 5 * 60 * 1000

                    # Split the audio file into segments
                    segments = [audio[i:i + segment_duration] for i in range(0, len(audio), segment_duration)]

                    # Save each segment as a separate file
                    segment_paths = []
                    for idx, segment in enumerate(segments):
                        segment_path = f"{temp_file_path}_segment_{idx}.mp3"
                        segment.export(segment_path, format="mp3")
                        segment_paths.append(segment_path)

                    # # Display the paths of the saved segments
                    # st.write("Segments saved at:")
                    # for path in segment_paths:
                    #     st.write(path)

    #######################################################################################################################################################################
    #########################################################  Initial Transcription using "Whisper-1" model  #############################################################
    #######################################################################################################################################################################

                    # Transcribe each segment
                    transcriptions = [transcribe_segment(path) for path in segment_paths]

                    # Combine all transcriptions into a single transcript
                    full_transcription = " ".join(transcriptions)
                    # st.write(full_transcription)


    #######################################################################################################################################################################
    ######################################################  Improving Reliability using Post-processing with GPT-4 model  #################################################
    #######################################################################################################################################################################

                    # Correct each transcription
                    corrected_transcriptions = [correct_transcription(transcription,desc,speakers) for transcription in transcriptions]

                    # Combine all corrected transcriptions into a single transcript
                    full_corrected_transcription = " ".join(corrected_transcriptions)
                    #st.write(full_corrected_transcription)
    
    #######################################################################################################################################################################
    ######################################################  Summarize the transcription's content  ########################################################################
    #######################################################################################################################################################################

                    summary=summarize_transcription(full_corrected_transcription)
                    #st.write(summary)
                

    #######################################################################################################################################################################
    ############################################################################  Results  ################################################################################
    #######################################################################################################################################################################
                    
                    #Show the Results directly on the app's interface
                    st.subheader("4.Results:")
                    st.write("")
                    st.subheader("Summary:")
                    st.write(summary)
                    st.subheader("Full Transcription:")
                    st.write(full_corrected_transcription)

                    buffer=docx_creation(summary,full_corrected_transcription)

                    #Download button
                    st.download_button(
                        label="Download Results",
                        data=buffer,
                        file_name="Transcription Results.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

