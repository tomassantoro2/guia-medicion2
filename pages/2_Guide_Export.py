"""Guide queue, review, duplicate, remove, and Excel export."""

import copy
import io
from datetime import datetime
from typing import List, Tuple

import pandas as pd
import streamlit as st

from measurement_guide.excel_export import build_measurement_workbook
from measurement_guide.models import normalize_event_record
from measurement_guide.ui_theme import (
    apply_editorial_styles,
    render_theme_toggle_header,
    step_title,
)


def _pairs_from_dataframe(df) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    if df is None or df.empty:
        return out
    for _, row in df.iterrows():
        k = str(row.get("Key", "") or "").strip()
        v = str(row.get("Value", "") or "").strip()
        if k or v:
            out.append((k, v))
    return out


st.set_page_config(
    page_title="Guide & export",
    layout="wide",
    initial_sidebar_state="collapsed",
)
render_theme_toggle_header()
apply_editorial_styles()

st.title("Guide queue & export")
st.caption("Review events, duplicate or remove rows, download the Excel guide.")

if "events" not in st.session_state:
    st.session_state.events = []

events = st.session_state.events

if not events:
    st.info("No events in the guide yet. Add events from the **Home** page.")
else:
    with st.container(border=True):
        st.markdown(
            step_title(1, "Reference & download", "Optional key/value rows + Excel file"),
            unsafe_allow_html=True,
        )
        st.caption(
            "These rows appear on the **Guide overview** sheet (Key / Value). "
            "Use them for site-wide notes, property IDs, or any extra context."
        )
        if "guide_ref_df" not in st.session_state:
            st.session_state.guide_ref_df = pd.DataFrame(
                [{"Key": "", "Value": ""}],
                columns=["Key", "Value"],
            )

        edited_df = st.data_editor(
            st.session_state.guide_ref_df,
            num_rows="dynamic",
            use_container_width=True,
            key="guide_ref_editor",
            hide_index=True,
        )
        st.session_state.guide_ref_df = edited_df.copy()

        ref_pairs = _pairs_from_dataframe(edited_df)

        buf = build_measurement_workbook(
            [normalize_event_record(e) for e in events],
            reference_pairs=ref_pairs if ref_pairs else None,
        )
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Download Excel (measurement guide)",
            data=buf.getvalue(),
            file_name=f"measurement_guide_{ts}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            key="download_excel_page",
        )

    with st.container(border=True):
        st.markdown(
            step_title(2, "Events in this guide", "Expand a row to duplicate, remove, or inspect"),
            unsafe_allow_html=True,
        )
        for i, ev in enumerate(events):
            title = f"Event {i + 1}: {ev.get('ga4_event_name') or ev.get('datalayer', {}).get('event_name', 'event')}"
            with st.expander(title):
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("Duplicate", key=f"dup_{i}", help="Append a copy to the guide"):
                        st.session_state.events.append(copy.deepcopy(normalize_event_record(ev)))
                        st.rerun()
                with c2:
                    if st.button("Remove", key=f"rm_{i}", type="secondary"):
                        st.session_state.events.pop(i)
                        st.rerun()

                if ev.get("screenshot"):
                    st.image(io.BytesIO(ev["screenshot"]), caption="Screenshot", width=240)

                st.write("**Page / URL:**", ev.get("page_url") or "—")
                st.write("**Environment:**", ev.get("environment") or "—")
                st.write("**GA4 event (recommended):**", ev.get("ga4_event_name") or "—")
                st.write("**Notes:**", ev.get("notes") or "—")
                st.write("**How it is triggered:**")
                st.write(ev.get("how") or "—")
                st.write("**Element type:**", ev.get("type") or "—")
                st.write("**dataLayer:**")
                st.json(ev.get("datalayer") or {})
