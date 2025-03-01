import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pdfplumber
import webbrowser
import os
import datetime
from typing import Dict, List, Tuple
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

class PDFProcessor:
    def __init__(self):
        self.current_language = 'en'  # 默认使用中文
        self.translations = {
            'zh': {
                'title': 'PDF处理工具',
                'select_file': '选择PDF文件',
                'extract_links': '提取链接',
                'extract_annotations': '提取注释',
                'switch_language': '切换语言 (Switch Language)',
                'no_file': '请先选择PDF文件',
                'processing': '处理中...',
                'success': '处理完成',
                'error': '处理出错',
                'none': '无',
                'table_no': '序号',
                'table_page': '页码',
                'table_submitter': '提交人',
                'table_content': '内容',
                'table_comment': '批注',
                'table_link': '链接',
                'info': '提示',
                'warning': '警告'
            },
            'en': {
                'title': 'PDF Processor',
                'select_file': 'Select PDF File',
                'extract_links': 'Extract Links',
                'extract_annotations': 'Extract Annotations',
                'switch_language': '切换语言 (Switch Language)',
                'no_file': 'Please select a PDF file first',
                'processing': 'Processing...',
                'success': 'Processing completed',
                'error': 'Error occurred',
                'none': 'None',
                'table_no': 'No.',
                'table_page': 'Page',
                'table_submitter': 'Submitter',
                'table_content': 'Content',
                'table_comment': 'Comment',
                'table_link': 'Link',
                'info': 'Information',
                'warning': 'Warning'
            }
        }
        self.pdf_file = None
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title(self.get_text('title'))
        self.root.geometry('400x300')

        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 文件选择按钮
        self.select_btn = ttk.Button(
            main_frame,
            text=self.get_text('select_file'),
            command=self.select_file
        )
        self.select_btn.grid(row=0, column=0, columnspan=2, pady=5)

        # 文件路径显示
        self.file_label = ttk.Label(main_frame, text="")
        self.file_label.grid(row=1, column=0, columnspan=2, pady=5)

        # 提取链接按钮
        self.extract_links_btn = ttk.Button(
            main_frame,
            text=self.get_text('extract_links'),
            command=self.extract_links
        )
        self.extract_links_btn.grid(row=2, column=0, pady=5)

        # 提取注释按钮
        self.extract_annotations_btn = ttk.Button(
            main_frame,
            text=self.get_text('extract_annotations'),
            command=self.extract_annotations
        )
        self.extract_annotations_btn.grid(row=2, column=1, pady=5)

        # 语言切换按钮
        self.lang_btn = ttk.Button(
            main_frame,
            text=self.get_text('switch_language'),
            command=self.switch_language
        )
        self.lang_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def get_text(self, key: str) -> str:
        return self.translations[self.current_language][key]

    def select_file(self):
        self.pdf_file = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if self.pdf_file:
            self.file_label.config(text=os.path.basename(self.pdf_file))

    def switch_language(self):
        self.current_language = 'en' if self.current_language == 'zh' else 'zh'
        # 更新UI文本
        self.root.title(self.get_text('title'))
        self.select_btn.config(text=self.get_text('select_file'))
        self.extract_links_btn.config(text=self.get_text('extract_links'))
        self.extract_annotations_btn.config(text=self.get_text('extract_annotations'))
        self.lang_btn.config(text=self.get_text('switch_language'))

    def get_link_text(self, pdf_path: str, page_num: int, rect: List[float]) -> str:
        """从指定页面和区域提取链接文本"""
        link_text = ""
        try:
            for page_layout in extract_pages(pdf_path, page_numbers=[page_num-1]):
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        # 检查文本元素是否在链接区域内
                        if (rect[0] <= element.x0 <= rect[2] and
                            rect[1] <= element.y0 <= rect[3]):
                            link_text += element.get_text().strip()
        except Exception as e:
            print(f"提取链接文本时出错: {e}")
        return link_text

    def extract_links(self):
        if not self.pdf_file:
            messagebox.showwarning(self.get_text('warning'), self.get_text('no_file'))
            return

        try:
            links = []
            with pdfplumber.open(self.pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    for annot in page.annots:
                        if annot.get("uri"):
                            print("完整数据", annot)
                            uri = annot["uri"]
                            content = annot.get("contents")  # 首选contents属性
                            
                            if not content:
                                # 使用PDFMiner的布局分析功能提取链接区域文本
                                # 优先使用annot对象的坐标属性
                                rect = [annot.get('x0', 0), annot.get('y0', 0), 
                                       annot.get('x1', 0), annot.get('y1', 0)]
                                
                                # 如果坐标属性不存在，尝试从data.Rect获取
                                if all(v == 0 for v in rect) and 'data' in annot:
                                    rect = annot['data'].get('Rect', [])
                                
                                if len(rect) == 4:
                                    print(f"链接区域坐标：{rect}")
                                    content = self.get_link_text(self.pdf_file, page_num, rect)
                                if not content:
                                    content = f"链接{rect}"
                                                 
                            links.append((page_num, content, uri))

            print("提取的链接数据：", links)
            self.generate_html('links', links)
            messagebox.showinfo(self.get_text('info'), self.get_text('success'))

        except Exception as e:
            print(f"提取链接时出错：{str(e)}")
            messagebox.showerror(self.get_text('error'), f"{self.get_text('error')}: {str(e)}")

    def extract_annotations(self):
        if not self.pdf_file:
            messagebox.showwarning(self.get_text('warning'), self.get_text('no_file'))
            return

        try:
            annotations = []
            with pdfplumber.open(self.pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    for annot in page.annots:
                        title = annot.get('title')
                        if title is not None:
                            content = annot.get('contents', self.get_text('none'))
                            author = annot.get('title', annot.get('author', self.get_text('none')))
                            annotations.append((page_num, author, content))

            print("提取的注释数据：", annotations)
            self.generate_html('annotations', annotations)
            messagebox.showinfo(self.get_text('info'), self.get_text('success'))

        except Exception as e:
            print(f"提取注释时出错：{str(e)}")
            messagebox.showerror(self.get_text('error'), f"{self.get_text('error')}: {str(e)}")

    def generate_html(self, type_: str, data: List[Tuple]):
        print(f"开始生成HTML，类型：{type_}，数据：", data)
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>PDF {type_}</title>
            <style>
                table {{ border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                a {{ color: #0066cc; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                h1 {{ color: #333; font-size: 24px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>{filename}</h1>
            <table>
                <thead>
                    <tr>
                        {headers}
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
        </html>
        """

        if type_ == 'links':
            headers = f"<th>{self.get_text('table_no')}</th><th>{self.get_text('table_page')}</th><th>{self.get_text('table_content')}</th><th>{self.get_text('table_link')}</th>"
            rows = ""
            for idx, (page, content, uri) in enumerate(data, 1):
                rows += f"<tr><td>{idx}</td><td>{page}</td><td>{content}</td>"
                if uri != self.get_text('none'):
                    rows += f"<td><a href='{uri}'>{uri}</a></td></tr>"
                else:
                    rows += f"<td>{uri}</td></tr>"
        else:  # annotations
            headers = f"<th>{self.get_text('table_no')}</th><th>{self.get_text('table_page')}</th><th>{self.get_text('table_submitter')}</th><th>{self.get_text('table_comment')}</th>"
            rows = ""
            for idx, (page, author, content) in enumerate(data, 1):
                rows += f"<tr><td>{idx}</td><td>{page}</td><td>{author}</td><td>{content}</td></tr>"

        html_content = html_template.format(
            headers=headers,
            rows=rows,
            type_=type_,
            filename=os.path.basename(self.pdf_file)
        )
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = "readlinks" if type_ == "links" else "readcomments"
        output_file = os.path.join(os.path.dirname(self.pdf_file), f"{prefix}_{current_time}.html")

        print(f"生成的HTML文件路径：{output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        webbrowser.open(output_file)

def main():
    app = PDFProcessor()
    app.root.mainloop()

if __name__ == "__main__":
    main()