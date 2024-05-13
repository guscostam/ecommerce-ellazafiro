from flask import Blueprint, render_template, redirect, url_for, session, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pandas as pd
import sqlite3

reports_bp = Blueprint('reports', __name__)

def fetch_data_from_sqlite(database_file, table_name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()
    conn.close()
    return data

@reports_bp.route('/download_excel_products')
def download_excel_products():
    if 'username' in session:
        username = session['username']
        database_file = f"data/user_{username}.db"
        table_name = "products"
        data = fetch_data_from_sqlite(database_file, table_name)
        df = pd.DataFrame(data, columns=["ID", "Nome do Produto", "Preço", "Tamanho", "Cor"])
        excel_file = "products.xlsx"
        df.to_excel(excel_file, index=False)
        return send_file(excel_file, as_attachment=True)
    else:
        return redirect(url_for('login.index_login'))

@reports_bp.route('/download_pdf_products')
def download_pdf_products():
    if 'username' in session:
        username = session['username']
        database_file = f"data/user_{username}.db"
        table_name = "products"
        data = fetch_data_from_sqlite(database_file, table_name)

        pdf_file = "products.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        table_data = [["ID", "Nome do Produto", "Preço", "Tamanho", "Cor"]] + list(data)
        table = Table(table_data)

        style = TableStyle([('BACKGROUND', (0,0), (-1,0), (0.8, 0.8, 0.8)),
                            ('TEXTCOLOR',(0,0),(-1,0),(0, 0, 0)),
                            ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0,0), (-1,0), 12),
                            ('BACKGROUND', (0,1), (-1,-1), (0.9, 0.9, 0.9)),
                            ('GRID',(0,0),(-1,-1),1,(0, 0, 0))])
        table.setStyle(style)

        elements = [table]
        doc.build(elements)
        return send_file(pdf_file, as_attachment=True)
    else:
        return redirect(url_for('login.index_login'))

@reports_bp.route('/download_excel_clients')
def download_excel_clients():
    if 'username' in session:
        username = session['username']
        database_file = f"data/user_{username}.db"
        table_name = "clients"
        data = fetch_data_from_sqlite(database_file, table_name)
        df = pd.DataFrame(data, columns=["ID", "Nome", "Sobrenome", "E-mail", "Número de Telefone", "Endereço"])
        excel_file = "clients.xlsx"
        df.to_excel(excel_file, index=False)
        return send_file(excel_file, as_attachment=True)

@reports_bp.route('/download_pdf_clients')
def download_pdf_clients():
    if 'username' in session:
        username = session['username']
        database_file = f"data/user_{username}.db"
        table_name = "clients"
        data = fetch_data_from_sqlite(database_file, table_name)

        pdf_file = "clients.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        table_data = [["ID", "Nome", "Sobrenome", "E-mail", "Número de Telefone", "Endereço"]] + list(data)
        table = Table(table_data)

        style = TableStyle([('BACKGROUND', (0,0), (-1,0), (0.8, 0.8, 0.8)),
                            ('TEXTCOLOR',(0,0),(-1,0),(0, 0, 0)),
                            ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0,0), (-1,0), 12),
                            ('BACKGROUND', (0,1), (-1,-1), (0.9, 0.9, 0.9)),
                            ('GRID',(0,0),(-1,-1),1,(0, 0, 0))])
        table.setStyle(style)

        elements = [table]
        doc.build(elements)
        return send_file(pdf_file, as_attachment=True)
    else:
        return redirect(url_for('login.index_login'))
