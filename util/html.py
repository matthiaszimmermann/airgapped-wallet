import base64
from io import BytesIO

class HtmlUtility:
    NEWLINE = '\n'

    HTML = "html"
    HEAD = "head"
    TITLE = "title"
    STYLE = "style"
    BODY = "body"
    DIV = "div"
    H2 = "h2"
    P = "p"
    FOOTER = "footer"

    @staticmethod
    def add_title(buf: list, title: str):
        HtmlUtility.add_element_with_content(buf, HtmlUtility.TITLE, title)

    @staticmethod
    def add_styles(buf: list, *styles: str):
        HtmlUtility.add_open_elements_with_class(buf, HtmlUtility.STYLE)
        for style in styles:
            buf.append(style)
            buf.append(HtmlUtility.NEWLINE)
        HtmlUtility.add_close_elements(buf, HtmlUtility.STYLE)

    @staticmethod
    def add_header2(buf: list, title: str):
        HtmlUtility.add_element_with_content(buf, HtmlUtility.H2, title)

    @staticmethod
    def add_paragraph(buf: list, paragraph: str, css_class: str = None):
        HtmlUtility.add_element_with_content(buf, HtmlUtility.P, paragraph, css_class)

    @staticmethod
    def add_content(buf: list, content: str):
        if content:
            buf.append(content)

    @staticmethod
    def add_element_with_content(buf: list, element: str, content: str, css_class: str = None):
        if not content:
            return
        if not element:
            raise ValueError("Tag of element to add must not be empty or null")
        HtmlUtility.add_open_elements_with_class(buf, element, css_class=css_class)
        buf.append(content)
        HtmlUtility.add_close_elements(buf, element)

    @staticmethod
    def add_encoded_image(buf: list, image: BytesIO, height: int, css_class: str = None):
        try:
            data = image.read()
            HtmlUtility.add_encoded_image_bytes(buf, data, height, css_class)
        except Exception as e:
            raise RuntimeError("Failed to load content from file input stream:", e)

    @staticmethod
    def add_encoded_image_bytes(buf: list, image_file: bytes, height: int, css_class: str = None):
        encoded_file = HtmlUtility.get_encoded_bytes(image_file)
        encoded_image = f'<img class="{css_class}" src="data:image/png;base64,{encoded_file}">\n'
        buf.append(encoded_image)

    @staticmethod
    def add_open_div(buf: list, *class_attributes: str):
        classes = " ".join(class_attributes)
        buf.append(f'<{HtmlUtility.DIV} class="{classes}">\n')

    @staticmethod
    def add_close_div(buf: list):
        HtmlUtility.add_close_elements(buf, HtmlUtility.DIV)

    @staticmethod
    def add_open_footer(buf: list, *class_attributes: str):
        classes = " ".join(class_attributes)
        buf.append(f'<{HtmlUtility.FOOTER} class="{classes}">\n')

    @staticmethod
    def add_close_footer(buf: list):
        HtmlUtility.add_close_elements(buf, HtmlUtility.FOOTER)

    @staticmethod
    def add_open_elements(buf: list, *elements: str):
        HtmlUtility.add_open_elements_with_class(buf, *elements)

    @staticmethod
    def add_open_elements_with_class(buf: list, *elements: str, css_class: str = None):
        for element in elements:
            buf.append(HtmlUtility.to_open_element(element, css_class))

    @staticmethod
    def add_close_elements(buf: list, *elements: str):
        for element in elements:
            buf.append(HtmlUtility.to_close_element(element))

    @staticmethod
    def get_encoded_bytes(data: bytes) -> str:
        return base64.b64encode(data).decode('utf-8')

    @staticmethod
    def to_open_element(element: str, css_class: str = None) -> str:
        if not css_class:
            return f'<{element}>\n'
        else:
            return f'<{element} class="{css_class}">\n'

    @staticmethod
    def to_close_element(element: str) -> str:
        return f'</{element}>\n'
