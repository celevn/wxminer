from lxml import etree


def parse_xml_msg(msg: str, path="appmsg/type", attr=None):
    """
    Function to parse messages in xml format

    Args:
        msg: str, xml message to parse
        path: certain xpath text to extract
        attr: if the info text lies in attribute list instead of xpath texts

    Returns:
        infomation text or None
    """
    try:
        xml = etree.XML(
            text=msg,  # assign parser to bypass xml errors
            parser=etree.XMLParser(remove_blank_text=True, recover=True)
        )
        ele = xml.xpath(path)[0]
        info = ele.get(attr) if attr else ele.text
        if info == "":
            info = None
    except:
        info = None
    return info
