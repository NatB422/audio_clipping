from pathlib import Path
import tempfile
import time
import streamlit as st

from library.snippet import Snippet, extract_snippet, extract_multiple_snippets


@st.dialog("Add snippet")
def add_snippet():
    start = st.number_input("Start time (seconds)", min_value=0.0, value=0.0, step=0.1)
    col_widths = [0.4, 0.6]
    col1, col2 = st.columns(col_widths)
    end = None
    if not col1.checkbox("to End", value=True):
        end = col2.number_input("End time (seconds)", step=0.1)

    col1, col2 = st.columns(col_widths)
    fade_in = None
    if col1.checkbox("Fade in"):
        fade_in = col2.number_input("Fade in duration (seconds)", min_value=0.0, value=0.0, step=0.1)

    col1, col2 = st.columns(col_widths)
    fade_out = None
    if col1.checkbox("Fade out"):
        fade_out = col2.number_input("Fade out duration (seconds)", min_value=0.0, value=0.0, step=0.1)

    if st.button("Add"):
        st.session_state.snippets.append(Snippet(start, end, fade_in, fade_out))
        st.rerun()

@st.fragment()
def snippet_management():
    # Snippet Management
    st.subheader("Snippets to clip")
    st.dataframe(st.session_state.snippets, hide_index=True)
    col1, col2, col3 = st.columns(3)
    if col1.button("Add snippet"):
        add_snippet()
    if col2.button("Delete last"):
        if st.session_state.snippets:
            st.session_state.snippets.pop()
            st.rerun()
    if col3.button("Clear snippets"):
        st.session_state.snippets.clear()
        st.rerun()


def run_process(filedata:bytes):

    input_file = tempfile.NamedTemporaryFile(delete=False)
    output_file = tempfile.NamedTemporaryFile(delete=False)

    try:
        input_file.write(filedata)
        if len(st.session_state.snippets) == 1:
            # Single part, so handle directly
            snippet = st.session_state.snippets[0]
            extract_snippet(Path(input_file.name), snippet, Path(output_file.name))
        else:
            progress = st.progress(0, "Clipping in progress")
            def progress_callback(percentage:float):
                progress.progress(percentage)

            # Multiple files, so need to handle with parts
            snippets = st.session_state.snippets.copy()
            extract_multiple_snippets(Path(input_file.name), Path(output_file.name), snippets, part_completion_callback=progress_callback)

            del snippets
            time.sleep(1)
            progress.empty()

        output_data = output_file.read()
    finally:
        input_file.close()
        if Path(input_file.name).exists():
            Path(input_file.name).unlink()

        output_file.close()
        if Path(output_file.name).exists():
            Path(output_file.name).unlink()

    return output_data


def main():
    st.title("Audio Clipper")

    if "snippets" not in st.session_state:
        st.session_state["snippets"] = []

    supercol1, supercol2 = st.columns([0.55, 0.45])
    # File upload
    with supercol1:
        st.subheader("File to be processed")
        uploaded_file = st.file_uploader("Upload", )

    with supercol2:
        snippet_management()

    # Run the process
    st.subheader("Output")
    col1, col2 = st.columns(2)
    output_data = None
    run_btn = col1.button("Run process")
    if run_btn:
        input_data = uploaded_file.read()
        output_data = run_process(input_data)

    if output_data:
        input_filename = uploaded_file.name # type: str
        input_filename_without_ext = input_filename[:input_filename.rfind(".")]
        output_filename = f"{input_filename_without_ext}_processed.mp3"
        col2.download_button(f"Download {output_filename}", output_data, output_filename)


if __name__ == "__main__":
    main()
