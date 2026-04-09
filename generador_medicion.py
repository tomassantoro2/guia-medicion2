"""
Measurement Guide Generator — Streamlit entry (Home).
Use the sidebar to open **Guide & export** for the queue and Excel download.
"""

import pandas as pd
import streamlit as st

from measurement_guide.catalog_loader import (
    catalog_choices,
    load_ga4_templates,
    load_mtp_for_entry,
)
from measurement_guide.datalayer_builders import build_measurement_script_preview
from measurement_guide.models import normalize_event_record
from measurement_guide.ui_theme import (
    apply_editorial_styles,
    render_new_event_start_focus_if_needed,
    render_theme_toggle_header,
    step_title,
)

st.set_page_config(
    page_title="Measurement Guide – Home",
    layout="wide",
    initial_sidebar_state="collapsed",
)
render_theme_toggle_header()
apply_editorial_styles()

if "events" not in st.session_state:
    st.session_state.events = []

if "extra_params" not in st.session_state:
    st.session_state.extra_params = []

catalog_entries, source_labels = catalog_choices()
ga4_templates_all = load_ga4_templates()

st.title("Measurement Guide Generator")
st.caption("Phase 2 · Custom · GA4 templates · MTP catalogs · dataLayer.push")
st.page_link("pages/2_Guide_Export.py", label="Open Guide & export", icon="📥")

with st.container(border=True):
    st.markdown(
        step_title(1, "Context", "Fill once — applies to events you add"),
        unsafe_allow_html=True,
    )
    col_a, col_b = st.columns(2)
    with col_a:
        page_url = st.text_input(
            "Page / URL (where to implement)",
            placeholder="e.g. https://example.com/checkout or /products/*",
            key="page_url",
        )
    with col_b:
        environment = st.selectbox(
            "Environment",
            ["", "production", "staging", "development"],
            key="environment",
        )

    notes = st.text_area(
        "Notes (ticket, sprint, owner, QA…)",
        placeholder="Optional",
        key="notes_event",
        height=68,
    )

with st.container(border=True):
    st.markdown(
        step_title(
            2,
            "Event setup",
            "GA4 doc column (optional), source, element, how it fires, screenshot",
        ),
        unsafe_allow_html=True,
    )
    ga4_metadata_name = st.text_input(
        "GA4 event name (recommended) — documentation column",
        placeholder="e.g. generate_lead (optional override)",
        key="ga4_metadata_name",
        help="Shown in Excel for alignment with GA4 recommended events. Does not replace the dataLayer snippet.",
    )
    event_source = st.radio(
        "Event source",
        source_labels,
        key="event_source",
        horizontal=True,
    )

    using_custom = event_source == "Custom event"
    using_ga4 = event_source == "GA4 recommended template"
    using_mtp = not using_custom and not using_ga4

    mtp_events = []
    mtp_entry = None
    if using_mtp:
        mtp_entry = next((e for e in catalog_entries if e.get("label") == event_source), None)
        if mtp_entry:
            mtp_events = load_mtp_for_entry(mtp_entry)

    event_type = st.selectbox(
        "Element type",
        ["Button", "Banner", "Link"],
        key="event_type",
    )

    how_triggered = st.text_area(
        "How it is triggered",
        placeholder="e.g. When the user clicks the Hot Sale button on the home page",
        key="how_triggered",
    )

    screenshot_file = st.file_uploader(
        "Screenshot",
        type=["png", "jpg", "jpeg"],
        key="screenshot_upload",
        help="Included in the Excel Screenshot column.",
    )
    if screenshot_file is not None:
        st.image(screenshot_file, caption="Preview", width=200)

    render_new_event_start_focus_if_needed()

dl: dict = {}

with st.container(border=True):
    st.markdown(
        step_title(3, "Configure the payload", "MTP catalog, GA4 template, or custom fields"),
        unsafe_allow_html=True,
    )

    if using_mtp and mtp_events:
        _PAGE_SIZE = 12
        mtp_filter = st.text_input(
            "Search MTP events",
            key="mtp_search",
            placeholder="Filter by description or event_name…",
        )
        q = (mtp_filter or "").lower().strip()
        filtered = [
            (i, e)
            for i, e in enumerate(mtp_events)
            if not q
            or q in str(e.get("description", "")).lower()
            or q in str(e.get("event_name", "")).lower()
        ]
        n_match = len(filtered)
        if q:
            st.caption(
                f"Searching for: `{q}` — descriptions and **event_name** are matched (case-insensitive)."
            )

        if not filtered:
            st.warning("No MTP events match the filter. Clear the search or try other keywords.")
        else:
            _sig = f"{mtp_filter!s}|{n_match}"
            if st.session_state.get("_mtp_filter_sig") != _sig:
                st.session_state._mtp_filter_sig = _sig
                st.session_state.mtp_list_page = 0
                for _k in ("mtp_catalog_df", "mtp_radio_choice", "mtp_pick"):
                    st.session_state.pop(_k, None)

            n_pages = max(1, (n_match + _PAGE_SIZE - 1) // _PAGE_SIZE)
            page = int(st.session_state.get("mtp_list_page", 0))
            page = max(0, min(page, n_pages - 1))
            st.session_state.mtp_list_page = page

            start = page * _PAGE_SIZE
            chunk = filtered[start : start + _PAGE_SIZE]

            _chunk_sig = f"{page}|{start}|{len(chunk)}|{_sig}"
            if st.session_state.get("_mtp_chunk_sig") != _chunk_sig:
                st.session_state._mtp_chunk_sig = _chunk_sig
                st.session_state.pop("mtp_catalog_df", None)
                st.session_state.pop("mtp_radio_choice", None)

            col_tbl, col_detail = st.columns([1.15, 1], gap="large")

            with col_tbl:
                tbl_wrap = st.container()
                with tbl_wrap:
                    st.markdown("**Browse this page**")
                    table_rows = []
                    for j, (_, ev) in enumerate(chunk):
                        desc = str(ev.get("description", "")).replace("\n", " ")
                        if len(desc) > 100:
                            desc = desc[:97] + "…"
                        table_rows.append(
                            {
                                "#": start + j + 1,
                                "event_name": ev.get("event_name", ""),
                                "description (preview)": desc,
                            }
                        )
                    df_mtp = pd.DataFrame(table_rows)
                    mtp_table = st.dataframe(
                        df_mtp,
                        use_container_width=True,
                        hide_index=True,
                        height=min(400, 44 * (len(df_mtp) + 1)),
                        on_select="rerun",
                        selection_mode="single-row",
                        key="mtp_catalog_df",
                    )

                    local_idx = 0
                    rows_list = []
                    if hasattr(mtp_table, "selection") and mtp_table.selection is not None:
                        rows_list = list(getattr(mtp_table.selection, "rows", []) or [])
                    if not rows_list and "mtp_catalog_df" in st.session_state:
                        raw = st.session_state["mtp_catalog_df"]
                        if isinstance(raw, dict):
                            rows_list = list(raw.get("selection", {}).get("rows", []) or [])
                    if rows_list:
                        local_idx = max(0, min(int(rows_list[0]), len(chunk) - 1))

                    st.caption(
                        "Click a row to select it for the dataLayer preview. "
                        "Sorting the table may reset the selection."
                    )

                    nav_a, nav_b, nav_c = st.columns([1, 4, 1])
                    with nav_a:
                        if st.button("◀", disabled=page <= 0, key="mtp_prev_pg", help="Previous page"):
                            st.session_state.mtp_list_page = page - 1
                            st.session_state.pop("mtp_catalog_df", None)
                            st.rerun()
                    with nav_b:
                        st.caption(
                            f"Page {page + 1} / {n_pages} · "
                            f"{min(_PAGE_SIZE, n_match - page * _PAGE_SIZE)} events on this page"
                        )
                    with nav_c:
                        if st.button("▶", disabled=page >= n_pages - 1, key="mtp_next_pg", help="Next page"):
                            st.session_state.mtp_list_page = page + 1
                            st.session_state.pop("mtp_catalog_df", None)
                            st.rerun()

            with col_detail:
                _, mtp_event = chunk[local_idx]
                dl = dict(mtp_event["dl"])
                st.markdown("### Detail")
                st.markdown(f"#### `{mtp_event.get('event_name', '')}`")
                st.markdown(mtp_event.get("description", "") or "—")
                st.info(
                    "The **dataLayer.push** preview in step 4 uses the catalog `dl` for this event."
                )
                with st.expander("Raw catalog `dl` (reference)", expanded=True):
                    st.json(mtp_event.get("dl", {}))
    elif using_mtp and not mtp_events:
        st.error("MTP catalog is empty or missing. Check catalogs/manifest.json and JSON files.")

    elif using_ga4:
        if not ga4_templates_all:
            st.warning("No GA4 templates found (catalogs/ga4_recommended.json).")
        else:
            lab = [
                f"{t.get('ga4_event_name', t['id'])} — {t.get('description', '')}"
                for t in ga4_templates_all
            ]
            tidx = st.selectbox(
                "GA4 template",
                range(len(ga4_templates_all)),
                format_func=lambda i: lab[i],
                key="ga4_tpl_idx",
            )
            tpl = ga4_templates_all[tidx]
            dl = dict(tpl.get("dl", {}))

            st.markdown("#### Additional parameters")
            st.caption("Add name/value pairs merged into the template dataLayer.")
            colx1, colx2, colx3 = st.columns([2, 2, 1])
            with colx1:
                ek = st.text_input(
                    "Name",
                    key="extra_key_ga4",
                    label_visibility="collapsed",
                    placeholder="Parameter name",
                )
            with colx2:
                ev = st.text_input(
                    "Value",
                    key="extra_value_ga4",
                    label_visibility="collapsed",
                    placeholder="Parameter value",
                )
            with colx3:
                st.write("")
                if st.button("Add", key="add_extra_ga4"):
                    if ek and ev:
                        st.session_state.extra_params.append({"key": ek, "value": ev})
                        for k in ("extra_key_ga4", "extra_value_ga4"):
                            if k in st.session_state:
                                del st.session_state[k]
                        st.rerun()
            if st.session_state.extra_params:
                for i, p in enumerate(list(st.session_state.extra_params)):
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        st.text(p["key"])
                    with c2:
                        st.text(p["value"])
                    with c3:
                        if st.button("Remove", key=f"rm_ex_ga4_{i}"):
                            st.session_state.extra_params.pop(i)
                            st.rerun()
            for p in list(st.session_state.extra_params):
                dl[str(p["key"])] = str(p["value"])

    else:
        event_base = st.selectbox(
            "GTM transport (`event` field)",
            ["uaevent", "nievent", "socialInt", "Custom"],
            key="event_base",
        )

        if event_base == "Custom":
            event_value = st.text_input(
                "Custom event name",
                placeholder="e.g. my_custom_event",
                key="event_custom",
            )
        else:
            event_value = event_base

        event_name = st.text_input(
            "event_name",
            placeholder="e.g. button_click",
            key="event_name",
        )

        st.markdown("### Suggested parameters")
        st.caption(
            "Optional: leave blank to omit from dataLayer. Only non-empty values are included."
        )

        eventCategory = st.text_input(
            "eventCategory",
            placeholder="e.g. interaction",
            key="eventCategory",
        )
        eventAction = st.text_input(
            "eventAction",
            placeholder="e.g. click",
            key="eventAction",
        )
        eventLabel = st.text_input(
            "eventLabel",
            placeholder="Optional",
            key="eventLabel",
        )

        st.markdown("### Additional parameters")
        st.caption("Add as many as required. Enter name and value, then click Add.")

        col_extra1, col_extra2, col_extra3 = st.columns([2, 2, 1])
        with col_extra1:
            extra_key = st.text_input(
                "Name",
                key="extra_key",
                label_visibility="collapsed",
                placeholder="Parameter name",
            )
        with col_extra2:
            extra_value = st.text_input(
                "Value",
                key="extra_value",
                label_visibility="collapsed",
                placeholder="Parameter value",
            )
        with col_extra3:
            st.write("")
            if st.button("Add", key="add_extra_param"):
                if extra_key and extra_value:
                    st.session_state.extra_params.append({"key": extra_key, "value": extra_value})
                    if "extra_key" in st.session_state:
                        del st.session_state["extra_key"]
                    if "extra_value" in st.session_state:
                        del st.session_state["extra_value"]
                    st.rerun()

        if st.session_state.extra_params:
            st.caption("Added parameters:")
            for i, p in enumerate(st.session_state.extra_params):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.text(p["key"])
                with col2:
                    st.text(p["value"])
                with col3:
                    if st.button("Delete", key=f"del_param_{i}"):
                        st.session_state.extra_params.pop(i)
                        st.rerun()

        dl = {}
        if event_value:
            dl["event"] = str(event_value)
        if event_name:
            dl["event_name"] = str(event_name)
        _ec = (eventCategory or "").strip()
        if _ec:
            dl["eventCategory"] = _ec
        _ea = (eventAction or "").strip()
        if _ea:
            dl["eventAction"] = _ea
        _el = (eventLabel or "").strip()
        if _el:
            dl["eventLabel"] = _el
        for p in list(st.session_state.extra_params):
            dl[str(p["key"])] = str(p["value"])

with st.container(border=True):
    st.markdown(
        step_title(4, "Review & add", "Check the snippet, then add to the guide queue"),
        unsafe_allow_html=True,
    )
    st.markdown("#### dataLayer.push preview")
    st.code(build_measurement_script_preview(dl), language="javascript")

    if st.button("Add event to guide", type="primary"):
        valid = True
        err_msg = None

        if using_mtp:
            valid = bool(dl)
            if not valid:
                err_msg = "No dataLayer for the selected MTP event."
        elif using_ga4:
            valid = bool(dl)
            if not valid:
                err_msg = "Select a GA4 template or add parameters."
        else:
            ev_base = st.session_state.get("event_base", "")
            ev_custom = st.session_state.get("event_custom", "")
            ev_name = st.session_state.get("event_name", "")
            event_value = ev_custom if ev_base == "Custom" else ev_base
            valid = bool(event_value) and bool(ev_name)
            if ev_base == "Custom" and not ev_custom:
                valid = False
            if not valid:
                if not event_value:
                    err_msg = "Please define the transport event (uaevent, custom, …)."
                elif not ev_name:
                    err_msg = "Please define event_name."
                elif ev_base == "Custom":
                    err_msg = "When Custom is selected, enter the custom event name."
                else:
                    err_msg = "Please complete the required fields."

        if not valid:
            st.error(err_msg)
        else:
            screenshot_bytes = screenshot_file.read() if screenshot_file else None
            gname = (st.session_state.get("ga4_metadata_name") or "").strip()
            if using_ga4 and ga4_templates_all:
                tidx = int(st.session_state.get("ga4_tpl_idx", 0))
                tpl = ga4_templates_all[tidx]
                if not gname:
                    gname = tpl.get("ga4_event_name", "")

            st.session_state.events.append(
                normalize_event_record(
                    {
                        "type": event_type,
                        "how": how_triggered,
                        "datalayer": dl,
                        "screenshot": screenshot_bytes,
                        "page_url": st.session_state.get("page_url") or "",
                        "environment": st.session_state.get("environment") or "",
                        "notes": st.session_state.get("notes_event") or "",
                        "ga4_event_name": gname,
                    }
                )
            )
            st.success("Event added. Open **Guide & export** in the sidebar to download Excel.")

            # Same for MTP, GA4, and Custom: after add, jump back to step 2 for the next event
            st.session_state._focus_new_event_start = True

            keys_to_clear = [
                "event_type",
                "how_triggered",
                "event_base",
                "event_custom",
                "event_name",
                "eventCategory",
                "eventAction",
                "eventLabel",
                "extra_key",
                "extra_value",
                "screenshot_upload",
                "ga4_metadata_name",
                "mtp_catalog_df",
                "mtp_radio_choice",
                "mtp_pick",
                "mtp_list_page",
                "_mtp_filter_sig",
                "_mtp_chunk_sig",
                "mtp_search",
                "ga4_tpl_idx",
                "extra_key_ga4",
                "extra_value_ga4",
            ]
            for key in keys_to_clear:
                st.session_state.pop(key, None)

            # MTP: clear any leftover session keys (selection/widget state) so reset matches GA4/custom
            for _k in list(st.session_state.keys()):
                if not isinstance(_k, str):
                    continue
                if (
                    _k.startswith("mtp_")
                    or _k.startswith("_mtp_")
                    or "mtp_catalog" in _k
                ):
                    st.session_state.pop(_k, None)

            st.session_state.extra_params = []
            st.rerun()
