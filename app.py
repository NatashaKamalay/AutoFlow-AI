import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from agents.extraction_agent import run_extraction
from agents.verification_agent import verify_analysis
from agents.decision_agent import enrich_analysis
from agents.audit_agent import log_event
from agents.monitor_agent import monitor_tasks
from agents.escalation_agent import generate_escalations
from utils.file_parser import extract_text_from_file
from rag.retriever import build_vectorstore
from rag.qa_agent import answer_question


def clear_workflow_state():
    keys_to_clear = [
        "analysis",
        "verification",
        "risk_report",
        "escalation_report",
        "vectorstore",
        "transcript_ready"
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


st.set_page_config(
    page_title="AutoFlow AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AutoFlow AI")
st.subheader("Autonomous Meeting & Workflow Intelligence")
st.caption(
    "Transforms unstructured meetings and documents into actionable workflows "
    "with risk detection, escalation, and contextual Q&A."
)

os.makedirs("uploads", exist_ok=True)

default_text = """
Project lead: We need the dashboard prototype by Friday.
Ananya will finalize the UI screens by Wednesday.
Rahul will connect the backend API by Thursday.
We agreed to delay the analytics module to phase 2.
Blocker: We still do not have client approval for the data schema.
Someone should follow up with the client tomorrow.
"""

with st.sidebar:
    st.header("Input Settings")
    input_mode = st.radio(
        "Choose input mode",
        ["Paste Transcript", "Upload Document"]
    )

if "last_input_mode" not in st.session_state:
    st.session_state["last_input_mode"] = input_mode

if st.session_state["last_input_mode"] != input_mode:
    clear_workflow_state()
    st.session_state["last_input_mode"] = input_mode

transcript = ""

if input_mode == "Paste Transcript":
    transcript = st.text_area(
        "Paste meeting transcript",
        value=default_text,
        height=250
    )

else:
    uploaded_file = st.file_uploader(
        "Upload a PDF, DOCX, or TXT file",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:
        if (
            "last_uploaded_file" not in st.session_state
            or st.session_state["last_uploaded_file"] != uploaded_file.name
        ):
            clear_workflow_state()
            st.session_state["last_uploaded_file"] = uploaded_file.name

        save_path = os.path.join("uploads", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            transcript = extract_text_from_file(save_path)
            st.markdown("### Extracted Document Text")
            st.text_area("Preview", value=transcript[:3000], height=250)

            log_event(
                "file_parser",
                "document_uploaded_and_parsed",
                {
                    "filename": uploaded_file.name,
                    "characters_extracted": len(transcript)
                }
            )
        except Exception as e:
            st.error(f"Failed to read uploaded file: {e}")

if st.button("Run Workflow", width="stretch"):
    try:
        if not transcript or not transcript.strip():
            st.warning("Please provide transcript text or upload a valid document.")
            st.stop()

        log_event("ui", "workflow_started", {"input_length": len(transcript)})

        analysis = run_extraction(transcript)
        log_event("extraction_agent", "extracted_meeting_data", analysis)

        analysis = enrich_analysis(analysis)
        log_event("decision_agent", "enriched_tasks", analysis)

        verification = verify_analysis(analysis)
        log_event("verification_agent", "verified_output", verification)

        risk_report = monitor_tasks(analysis)
        log_event("monitor_agent", "risk_analysis_completed", risk_report)

        escalation_report = generate_escalations(risk_report)
        log_event("escalation_agent", "escalation_generated", escalation_report)

        vectorstore = build_vectorstore(transcript)

        st.session_state["analysis"] = analysis
        st.session_state["verification"] = verification
        st.session_state["risk_report"] = risk_report
        st.session_state["escalation_report"] = escalation_report
        st.session_state["vectorstore"] = vectorstore

        log_event("rag_agent", "vectorstore_created", {"status": "success"})

        st.success("Workflow completed successfully.")

    except Exception as e:
        st.error(f"Workflow failed: {e}")
        log_event("system", "workflow_failed", {"error": str(e)})

if "analysis" in st.session_state:
    analysis = st.session_state["analysis"]
    verification = st.session_state["verification"]
    risk_report = st.session_state["risk_report"]
    escalation_report = st.session_state["escalation_report"]

    tasks = analysis.get("tasks", [])
    tasks_df = pd.DataFrame(tasks) if tasks else pd.DataFrame()

    total_tasks = len(tasks)
    ready_tasks = len([t for t in tasks if t.get("status") == "ready"])
    at_risk_tasks = len([t for t in tasks if t.get("status") == "at_risk"])
    blocker_count = len(analysis.get("blockers", []))

    st.markdown("## Workflow Dashboard")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Tasks", total_tasks)
    k2.metric("Ready Tasks", ready_tasks)
    k3.metric("At-Risk Tasks", at_risk_tasks)
    k4.metric("Blockers", blocker_count)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Overview", "Tasks", "Risks & Escalation", "Knowledge Q&A", "Analytics"]
    )

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Summary")
            st.write(analysis.get("summary", ""))

            st.markdown("### Decisions")
            decisions = analysis.get("decisions", [])
            if decisions:
                for d in decisions:
                    st.write(f"- {d}")
            else:
                st.info("No decisions found.")

        with col2:
            st.markdown("### Blockers")
            blockers = analysis.get("blockers", [])
            if blockers:
                for b in blockers:
                    st.write(f"- {b}")
            else:
                st.info("No blockers found.")

            st.markdown("### Verification Report")
            if verification["is_valid"]:
                st.success("All extracted tasks are sufficiently complete.")
            else:
                for issue in verification["issues"]:
                    st.warning(issue)

    with tab2:
        st.markdown("### Task Table")
        if not tasks_df.empty:
            st.dataframe(tasks_df, width="stretch")

            upcoming_df = tasks_df[["task", "owner", "deadline", "status"]].copy()
            st.markdown("### Upcoming Deadlines")
            st.dataframe(upcoming_df, width="stretch")
        else:
            st.info("No tasks found.")

    with tab3:
        st.markdown("### Risk Monitoring Report")
        if risk_report["risk_count"] == 0:
            st.success("No workflow risks detected.")
        else:
            for risk in risk_report["risks"]:
                st.error(f"{risk['severity'].upper()}: {risk['message']}")

        st.markdown("### Escalation Actions")
        if escalation_report["escalation_count"] == 0:
            st.success("No escalation needed.")
        else:
            for esc in escalation_report["escalations"]:
                st.info(
                    f"Task: {esc['task']} | Action: {esc['action']} | "
                    f"Level: {esc['level']} | Reason: {esc['reason']}"
                )

    with tab4:
        st.markdown("### Ask Follow-up Questions")
        question = st.text_input("Ask a question about the uploaded/pasted content")

        if st.button("Get Answer"):
            try:
                if "vectorstore" not in st.session_state:
                    st.warning("Please run the workflow first so the knowledge base can be created.")
                    st.stop()

                answer = answer_question(st.session_state["vectorstore"], question)

                log_event(
                    "qa_agent",
                    "question_answered",
                    {
                        "question": question,
                        "answer": answer
                    }
                )

                st.markdown("### Answer")
                st.write(answer)

            except Exception as e:
                st.error(f"Question answering failed: {e}")
                log_event("system", "qa_failed", {"error": str(e)})

    with tab5:
        st.markdown("### Task Status Distribution")
        if total_tasks > 0:
            status_counts = {
                "ready": ready_tasks,
                "at_risk": at_risk_tasks
            }

            fig, ax = plt.subplots()
            ax.bar(status_counts.keys(), status_counts.values())
            ax.set_ylabel("Count")
            ax.set_title("Task Status Overview")
            st.pyplot(fig)
        else:
            st.info("No tasks available for analytics.")

        st.markdown("### Risk Summary")
        st.write(f"Total risks detected: {risk_report['risk_count']}")
        st.write(f"Total escalations generated: {escalation_report['escalation_count']}")