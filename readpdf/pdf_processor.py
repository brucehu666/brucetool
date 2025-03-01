import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pdfplumber
import webbrowser
import os
import datetime
from typing import Dict, List, Tuple

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
                'info': '信息',
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
                            # 优化链接文本提取逻辑
                            content = annot.get("contents")  # 首选contents属性
                            if not content:  # 如果contents为空，尝试其他属性
                                # 尝试从Border属性中提取文本
                                Rect_text = annot.get("data", {}).get("Rect", [])
                                if Rect_text and isinstance(Rect_text, list):
                                    content = f"链接{Rect_text}"
                                else:
                                    # 如果没有任何文本信息，使用URI的一部分作为显示文本
                                    content = uri.split("/")[-1] if "/" in uri else uri
                            links.append((page_num, content, uri))

            print("提取的链接数据：", links)  # 添加调试输出
            self.generate_html('links', links)
            messagebox.showinfo(self.get_text('info'), self.get_text('success'))

        except Exception as e:
            print(f"提取链接时出错：{str(e)}")  # 添加错误详细信息
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

            print("提取的注释数据：", annotations)  # 添加调试输出
            self.generate_html('annotations', annotations)
            messagebox.showinfo(self.get_text('info'), self.get_text('success'))

        except Exception as e:
            print(f"提取注释时出错：{str(e)}")  # 添加错误详细信息
            messagebox.showerror(self.get_text('error'), f"{self.get_text('error')}: {str(e)}")

    def generate_html(self, type_: str, data: List[Tuple]):
        print(f"开始生成HTML，类型：{type_}，数据：", data)  # 添加调试输出
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
        # 获取当前时间，格式化为字符串
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # 根据类型选择前缀
        prefix = "readlinks" if type_ == "links" else "readcomments"
        output_file = os.path.join(os.path.dirname(self.pdf_file), f"{prefix}_{current_time}.html")

        print(f"生成的HTML文件路径：{output_file}")  # 添加调试输出
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        webbrowser.open(output_file)

def main():
    app = PDFProcessor()
    app.root.mainloop()

if __name__ == "__main__":
    main()