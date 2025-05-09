from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from env_config import logger
import tempfile
import os
import io
import json
import csv
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import subprocess

async def process_pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle PDF processing operations"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📄 Extract Text", callback_data="pdf_to_text"),
            InlineKeyboardButton("📎 To Word", callback_data="pdf_to_docx"),
        ],
        [
            InlineKeyboardButton("🔄 Merge PDFs", callback_data="merge_pdfs"),
            InlineKeyboardButton("✂️ Split PDF", callback_data="split_pdf"),
        ],
        [
            InlineKeyboardButton("📦 Compress", callback_data="compress_pdf"),
            InlineKeyboardButton("↩️ Back", callback_data="svc_back"),
        ]
    ]
    
    await query.message.edit_text(
        "📑 *PDF Processing Options:*\n\n"
        "• *Extract Text*: Get text content\n"
        "• *Convert to Word*: Create DOCX file\n"
        "• *Merge PDFs*: Combine multiple PDFs\n"
        "• *Split PDF*: Separate into pages\n"
        "• *Compress*: Reduce file size\n\n"
        "Choose an option or type your request!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def process_json_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle JSON processing operations"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📊 To CSV", callback_data="json_to_csv"),
            InlineKeyboardButton("📝 Format", callback_data="format_json"),
        ],
        [
            InlineKeyboardButton("✅ Validate", callback_data="validate_json"),
            InlineKeyboardButton("↩️ Back", callback_data="svc_back"),
        ]
    ]
    
    await query.message.edit_text(
        "🔤 *JSON Processing Options:*\n\n"
        "• *Convert to CSV*: Create spreadsheet\n"
        "• *Format JSON*: Prettify structure\n"
        "• *Validate*: Check syntax\n\n"
        "Choose an option or type your request!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def process_excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Excel/CSV processing operations"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📄 To PDF", callback_data="excel_to_pdf"),
            InlineKeyboardButton("📊 To CSV", callback_data="excel_to_csv"),
        ],
        [
            InlineKeyboardButton("📈 To JSON", callback_data="excel_to_json"),
            InlineKeyboardButton("↩️ Back", callback_data="svc_back"),
        ]
    ]
    
    await query.message.edit_text(
        "📊 *Spreadsheet Processing Options:*\n\n"
        "• *Convert to PDF*: Create PDF file\n"
        "• *Convert to CSV*: Create CSV file\n"
        "• *Convert to JSON*: Create JSON file\n\n"
        "Choose an option or type your request!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )