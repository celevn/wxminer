import streamlit as st


# 默认页名/图标/标题/描述/页脚
ST_PAGE_TITLE_DEFAULT = "WX Miner"
ST_PAGE_ICON_DEFAULT = "💬"
ST_HEADER_TITLE_DEFAULT = "WX Miner"
ST_HEADER_DESCRIPTION_DEFAULT = "重识微信聊天记录"
ST_FOOTER_CONTENT_DEFAULT = "Copyright © 2022, Celevn"
QR_GROUP_URL = "https://user-images.githubusercontent.com/10850975/189103222-ce5163df-e18a-4ea8-a963-7d1db945ccea.JPG"
QR_DONATE_URL = "https://user-images.githubusercontent.com/10850975/189103585-240ca79d-b3d9-46b7-9ee9-98a5051db706.PNG"


footer_html = """
    <style>
        footer {
            visibility: hidden;
        }
        footer:after {
            content: "%s";
            visibility: visible;
            display: block;
            text-align: center;
        }
    </style>
""" % ST_FOOTER_CONTENT_DEFAULT


def build_page(title=ST_PAGE_TITLE_DEFAULT,
               icon=ST_PAGE_ICON_DEFAULT,
               header=ST_HEADER_TITLE_DEFAULT,
               description=ST_HEADER_DESCRIPTION_DEFAULT,
               **kwargs) -> st.container:
    """
    Build a Streamlit page with fixed header/footer and return empty body

    Args:
        title: title of page tab
        icon: icon of page tab
        header: title on the page header
        description: detail text of header
        **kwargs: arguments to page config
    
    Returns:
        body: st.container to put main page content
    """
    # page configuration
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        initial_sidebar_state="expanded",
        menu_items={
            "Get help": QR_GROUP_URL,
            "About": f"""
                # WX Miner
                WeChat mining tool by [Celevn](https://github.com/celevn)
            """,
        },
        **kwargs
    )
    
    # header
    with st.container():
        st.title(header)
        if description:
            st.write(description)

    # body
    body = st.container()
    st.markdown("---")

    # footer
    with st.container():
        st.markdown(footer_html, unsafe_allow_html=True)

    return body