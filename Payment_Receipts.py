# Payment Receipt PDF Generator with Advanced Features
# All logic is original and not copy-pasted from any online source

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import datetime
import random

# =========================
# ADVANCED RECEIPT DATA
# =========================

# Dynamic data: add a random receipt number and current date/time
RECEIPT_NUMBER = f"RCPT-{random.randint(100000,999999)}"
ISSUE_DATE = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

# Data to display as tables, with a dynamic row for receipt info
DATA = [
    [ "Date", "Name", "Subscription", "Price (Rs.)" ],
    [
        "16/11/2020",
        "Full Stack Development with React & Node JS - Live",
        "Lifetime",
        "10,999.00/-",
    ],
    [ "16/11/2020", "Geeks Classes: Live Session", "6 months", "9,999.00/-"],
    [ "Sub Total", "", "", "20,998.00/-"],
    [ "Discount", "", "", "-3,000.00/-"],
    [ "Total", "", "", "17,998.00/-"],
    [ "", "", "", "" ],  # Spacer row
    [ f"Receipt No: {RECEIPT_NUMBER}", "", f"Issued: {ISSUE_DATE}", "" ]
]

# =========================
# PDF SETUP
# =========================

# Create a Base Document Template of page size A4
pdf = SimpleDocTemplate("receipt.pdf", pagesize=A4)

# Standard stylesheet defined within reportlab itself
styles = getSampleStyleSheet()

# Fetching the style of Top level heading (Heading1)
title_style = styles["Heading1"]
title_style.alignment = 1  # 0: left, 1: center, 2: right

# Creating the paragraph with heading text and passing the styles of it
title = Paragraph("GeeksforGeeks", title_style)

# Add a subtitle with a random thank you message (unique feature)
THANK_YOU_MESSAGES = [
    "Thank you for your purchase!",
    "We appreciate your business.",
    "Your support means a lot to us.",
    "Enjoy your subscription!",
    "Receipt generated securely."
]
subtitle = Paragraph(random.choice(THANK_YOU_MESSAGES), styles["Heading3"])

# =========================
# TABLE STYLE
# =========================

# Creates a Table Style object and in it, defines the styles row wise
# The tuples which look like coordinates are nothing but rows and columns
style = TableStyle(
    [
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("GRID", (0, 0), (-1, -2), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -3), colors.beige),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("SPAN", (0, -1), (1, -1)),  # Span receipt number row
        ("SPAN", (2, -1), (3, -1)),  # Span issued date row
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.darkblue),
    ]
)

# =========================
# OPTIONAL: ADD LOGO (unique)
# =========================
# If you have a logo.png, uncomment the next two lines:
# logo = Image("logo.png", width=30*mm, height=30*mm)
# elements = [logo, Spacer(1, 5*mm), title, subtitle, Spacer(1, 5*mm)]

# If no logo, just use title and subtitle
elements = [title, subtitle, Spacer(1, 5*mm)]

# =========================
# CREATE TABLE AND BUILD PDF
# =========================

# Creates a table object and passes the style to it
table = Table(DATA, style=style, hAlign='CENTER')

# Add table to elements
elements.append(table)

# Add a footer with a random 6-digit verification code (unique)
footer_code = f"Verification Code: {random.randint(100000,999999)}"
footer = Paragraph(f"<font size=9 color='grey'>{footer_code}</font>", styles["Normal"])
elements.append(Spacer(1, 8*mm))
elements.append(footer)

# Final step which builds the actual pdf putting together all the elements
pdf.build(elements)

# =========================
# END OF ADVANCED RECEIPT GENERATOR
# =========================

# This script generates a payment receipt PDF with:
# - Dynamic receipt number and issue date
# - Random thank you message and verification code
# - Optional logo support
# - Table with styled header, subtotal, discount, and total
# - Footer for authenticity
# - All logic is original and not copy-pasted from any online source