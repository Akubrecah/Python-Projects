import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
import datetime
from fpdf import FPDF

class AcademicTranscriptGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Academic Transcript Generator")
        master.geometry("900x700")
        master.configure(bg="#1e1e2d")
        master.resizable(True, True)
        
        # Create elegant theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#1e1e2d')
        self.style.configure('TLabel', background='#1e1e2d', foreground='#e0e0ff', font=('Helvetica', 10))
        self.style.configure('TButton', background='#3a3a5a', foreground='#e0e0ff', 
                            font=('Helvetica', 10, 'bold'), borderwidth=1)
        self.style.map('TButton', background=[('active', '#4a4a7a')])
        self.style.configure('Header.TLabel', font=('Georgia', 16, 'bold'), 
                            foreground='#d4af37', background='#1e1e2d')
        self.style.configure('Result.TLabel', font=('Helvetica', 12, 'bold'), 
                            foreground='#ffffff', background='#2a2a3a')
        self.style.configure('Subject.TLabel', font=('Helvetica', 11), 
                            foreground='#c0c0e0', background='#2a2a3a')
        
        # Create header frame
        self.header_frame = ttk.Frame(master, padding=(20, 10))
        self.header_frame.pack(fill=tk.X)
        
        # Title
        self.title_label = ttk.Label(self.header_frame, text="ACADEMIC TRANSCRIPT", 
                                    style='Header.TLabel')
        self.title_label.pack()
        
        # University crest placeholder (text-based)
        self.crest_label = ttk.Label(self.header_frame, text="◈", 
                                    font=('Helvetica', 24), 
                                    foreground='#d4af37', 
                                    background='#1e1e2d')
        self.crest_label.place(x=20, y=5)
        
        # Create student info frame
        self.info_frame = ttk.LabelFrame(master, text="Student Information", padding=15)
        self.info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Student information fields
        info_labels = ["Full Name:", "Student ID:", "Program:", "Department:", "Academic Year:"]
        self.info_entries = []
        
        for i, label_text in enumerate(info_labels):
            ttk.Label(self.info_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(self.info_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
            self.info_entries.append(entry)
        
        # Create transcript frame
        self.transcript_frame = ttk.LabelFrame(master, text="Course Performance", padding=15)
        self.transcript_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Transcript table headers
        headers = ["Course Code", "Course Title", "Credits", "Grade", "Grade Points"]
        for col, header in enumerate(headers):
            ttk.Label(self.transcript_frame, text=header, style='Subject.TLabel',
                      padding=5).grid(row=0, column=col, sticky=tk.W+tk.E, padx=2, pady=2)
        
        # Course entries
        self.course_entries = []
        courses = [
            ("CS201", "Data Structures & Algorithms", "4"),
            ("CS202", "Database Systems", "4"),
            ("MA201", "Advanced Calculus", "3"),
            ("EC201", "Digital Electronics", "4"),
            ("HU101", "Professional Ethics", "2")
        ]
        
        for row, (code, title, credits) in enumerate(courses, start=1):
            # Course code
            code_label = ttk.Label(self.transcript_frame, text=code, style='Subject.TLabel')
            code_label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
            
            # Course title
            title_label = ttk.Label(self.transcript_frame, text=title, style='Subject.TLabel')
            title_label.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
            
            # Credits
            credits_label = ttk.Label(self.transcript_frame, text=credits, style='Subject.TLabel')
            credits_label.grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
            
            # Grade entry
            grade_var = tk.StringVar()
            grade_combobox = ttk.Combobox(self.transcript_frame, textvariable=grade_var, 
                                         width=5, state='readonly')
            grade_combobox['values'] = ('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F')
            grade_combobox.current(0)
            grade_combobox.grid(row=row, column=3, padx=5, pady=5)
            
            # Grade points display
            points_label = ttk.Label(self.transcript_frame, text="", style='Subject.TLabel')
            points_label.grid(row=row, column=4, sticky=tk.W, padx=5, pady=5)
            
            self.course_entries.append((grade_var, points_label, int(credits)))
        
        # Results frame
        self.result_frame = ttk.Frame(master, padding=15)
        self.result_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Result labels
        ttk.Label(self.result_frame, text="Total Credits:", 
                 style='Result.TLabel').grid(row=0, column=0, padx=10, sticky=tk.W)
        self.total_credits_label = ttk.Label(self.result_frame, text="0", 
                                           style='Result.TLabel', font=('Helvetica', 12, 'bold'))
        self.total_credits_label.grid(row=0, column=1, padx=10, sticky=tk.W)
        
        ttk.Label(self.result_frame, text="Total Grade Points:", 
                 style='Result.TLabel').grid(row=0, column=2, padx=10, sticky=tk.W)
        self.total_points_label = ttk.Label(self.result_frame, text="0.00", 
                                          style='Result.TLabel', font=('Helvetica', 12, 'bold'))
        self.total_points_label.grid(row=0, column=3, padx=10, sticky=tk.W)
        
        ttk.Label(self.result_frame, text="GPA:", 
                 style='Result.TLabel').grid(row=0, column=4, padx=10, sticky=tk.W)
        self.gpa_label = ttk.Label(self.result_frame, text="0.00", 
                                  style='Result.TLabel', font=('Helvetica', 14, 'bold'))
        self.gpa_label.grid(row=0, column=5, padx=10, sticky=tk.W)
        
        ttk.Label(self.result_frame, text="Academic Standing:", 
                 style='Result.TLabel').grid(row=0, column=6, padx=10, sticky=tk.W)
        self.standing_label = ttk.Label(self.result_frame, text="", 
                                       style='Result.TLabel', font=('Helvetica', 12, 'bold'))
        self.standing_label.grid(row=0, column=7, padx=10, sticky=tk.W)
        
        # Button frame
        self.button_frame = ttk.Frame(master)
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Buttons
        ttk.Button(self.button_frame, text="Generate Transcript", 
                  command=self.generate_transcript).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.button_frame, text="Reset", 
                  command=self.reset_form).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.button_frame, text="Export to CSV", 
                  command=self.export_to_csv).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.button_frame, text="Export to PDF", 
                  command=self.export_to_pdf).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.button_frame, text="Exit", 
                  command=master.quit).pack(side=tk.RIGHT, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(master, textvariable=self.status_var, 
                                  relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set initial focus
        if self.info_entries:
            self.info_entries[0].focus_set()
    
    def grade_to_points(self, grade):
        """Convert letter grade to grade points"""
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'D': 1.0, 'F': 0.0
        }
        return grade_points.get(grade, 0.0)
    
    def generate_transcript(self):
        """Calculate and display transcript results"""
        # Validate student information
        if not all(entry.get().strip() for entry in self.info_entries[:2]):
            messagebox.showwarning("Missing Information", 
                                  "Please enter at least student name and ID.")
            return
        
        total_credits = 0
        total_points = 0.0
        
        # Process each course
        for grade_var, points_label, credits in self.course_entries:
            grade = grade_var.get()
            points = self.grade_to_points(grade)
            earned_points = points * credits
            
            # Update points display
            points_label.config(text=f"{earned_points:.1f}")
            
            total_credits += credits
            total_points += earned_points
        
        # Calculate GPA
        gpa = total_points / total_credits if total_credits else 0.0
        
        # Update results display
        self.total_credits_label.config(text=str(total_credits))
        self.total_points_label.config(text=f"{total_points:.1f}")
        self.gpa_label.config(text=f"{gpa:.2f}")
        
        # Determine academic standing
        if gpa >= 3.6:
            standing = "Dean's List"
            color = "#4caf50"  # Green
        elif gpa >= 2.0:
            standing = "Good Standing"
            color = "#2196f3"  # Blue
        else:
            standing = "Academic Probation"
            color = "#f44336"  # Red
        
        self.standing_label.config(text=standing, foreground=color)
        
        self.status_var.set("Transcript generated successfully")
    
    def reset_form(self):
        """Reset all fields to default values"""
        for entry in self.info_entries:
            entry.delete(0, tk.END)
        
        for grade_var, points_label, _ in self.course_entries:
            grade_var.set('A+')
            points_label.config(text="")
        
        self.total_credits_label.config(text="0")
        self.total_points_label.config(text="0.00")
        self.gpa_label.config(text="0.00")
        self.standing_label.config(text="")
        
        if self.info_entries:
            self.info_entries[0].focus_set()
        
        self.status_var.set("Form reset")
    
    def export_to_csv(self):
        """Export transcript data to CSV file"""
        # Check if we have student information
        if not all(entry.get().strip() for entry in self.info_entries[:2]):
            messagebox.showwarning("Missing Information", 
                                  "Please enter at least student name and ID before exporting.")
            return
        
        filename = f"Transcript_{self.info_entries[1].get()}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["Academic Transcript"])
                writer.writerow([])
                
                # Write student information
                writer.writerow(["Student Name:", self.info_entries[0].get()])
                writer.writerow(["Student ID:", self.info_entries[1].get()])
                writer.writerow(["Program:", self.info_entries[2].get()])
                writer.writerow(["Department:", self.info_entries[3].get()])
                writer.writerow(["Academic Year:", self.info_entries[4].get()])
                writer.writerow([])
                
                # Write course headers
                writer.writerow(["Course Code", "Course Title", "Credits", "Grade", "Grade Points"])
                
                # Write course data
                for i, ((grade_var, points_label, credits), course) in enumerate(zip(
                    self.course_entries, 
                    [("CS201", "Data Structures & Algorithms", "4"),
                     ("CS202", "Database Systems", "4"),
                     ("MA201", "Advanced Calculus", "3"),
                     ("EC201", "Digital Electronics", "4"),
                     ("HU101", "Professional Ethics", "2")])):
                    
                    code, title, _ = course
                    grade = grade_var.get()
                    points = points_label.cget("text") or "0.0"
                    
                    writer.writerow([code, title, credits, grade, points])
                
                # Write summary
                writer.writerow([])
                writer.writerow(["Total Credits:", self.total_credits_label.cget("text")])
                writer.writerow(["Total Grade Points:", self.total_points_label.cget("text")])
                writer.writerow(["GPA:", self.gpa_label.cget("text")])
                writer.writerow(["Academic Standing:", self.standing_label.cget("text")])
            
            self.status_var.set(f"Transcript exported to {filename}")
            messagebox.showinfo("Export Successful", 
                              f"Transcript has been exported to {os.path.abspath(filename)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export transcript: {str(e)}")
            self.status_var.set("Export failed")
    
    def export_to_pdf(self):
        """Export transcript data to PDF file"""
        # Validate student information
        if not all(entry.get().strip() for entry in self.info_entries[:2]):
            messagebox.showwarning("Missing Information", 
                                  "Please enter at least student name and ID before exporting.")
            return
        
        # Generate transcript if not already done
        if self.total_credits_label.cget("text") == "0":
            self.generate_transcript()
        
        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"Transcript_{self.info_entries[1].get()}"
        )
        
        if not filename:
            return  # User canceled
        
        try:
            # Create PDF document
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            
            # Set up colors
            primary_color = (30, 30, 45)    # Dark blue: #1e1e2d
            accent_color = (212, 175, 55)   # Gold: #d4af37
            text_color = (0, 0, 0)          # Black
            
            # Header with university information
            pdf.set_font('Helvetica', 'B', 16)
            pdf.set_text_color(*accent_color)
            pdf.cell(0, 10, "UNIVERSITY OF EXCELLENCE", ln=1, align='C')
            pdf.set_font('Helvetica', 'B', 14)
            pdf.cell(0, 8, "OFFICIAL ACADEMIC TRANSCRIPT", ln=1, align='C')
            
            # Divider
            pdf.set_draw_color(*accent_color)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(10)
            
            # Student information section
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(*primary_color)
            pdf.cell(0, 8, "STUDENT INFORMATION", ln=1)
            
            pdf.set_font('Helvetica', '', 11)
            pdf.set_text_color(*text_color)
            info_labels = ["Full Name:", "Student ID:", "Program:", "Department:", "Academic Year:"]
            
            for i, label in enumerate(info_labels):
                pdf.cell(45, 7, label)
                pdf.cell(0, 7, self.info_entries[i].get(), ln=1)
            
            pdf.ln(5)
            
            # Course performance section
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(*primary_color)
            pdf.cell(0, 8, "COURSE PERFORMANCE", ln=1)
            pdf.ln(2)
            
            # Table headers
            pdf.set_fill_color(*primary_color)
            pdf.set_text_color(255, 255, 255)  # White text
            pdf.set_font('Helvetica', 'B', 11)
            
            # Column widths
            col_widths = [25, 80, 20, 20, 30]
            
            # Header row
            headers = ["Code", "Course Title", "Credits", "Grade", "Points"]
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 8, header, border=1, fill=True)
            pdf.ln()
            
            # Table content
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(*text_color)
            fill = False
            
            courses = [
                ("CS201", "Data Structures & Algorithms", "4"),
                ("CS202", "Database Systems", "4"),
                ("MA201", "Advanced Calculus", "3"),
                ("EC201", "Digital Electronics", "4"),
                ("HU101", "Professional Ethics", "2")
            ]
            
            for i, ((grade_var, points_label, credits), course) in enumerate(zip(
                self.course_entries, courses)):
                
                code, title, _ = course
                grade = grade_var.get()
                points = points_label.cget("text") or "0.0"
                
                # Alternate row colors
                if fill:
                    pdf.set_fill_color(240, 240, 245)  # Light gray
                else:
                    pdf.set_fill_color(255, 255, 255)  # White
                
                # Course code
                pdf.cell(col_widths[0], 8, code, border='LTR', fill=fill)
                # Course title
                pdf.cell(col_widths[1], 8, title, border='LTR', fill=fill)
                # Credits
                pdf.cell(col_widths[2], 8, credits, border='LTR', align='C', fill=fill)
                # Grade
                pdf.cell(col_widths[3], 8, grade, border='LTR', align='C', fill=fill)
                # Points
                pdf.cell(col_widths[4], 8, points, border='LTR', align='C', fill=fill, ln=1)
                
                fill = not fill
            
            # Bottom border
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(sum(col_widths), 0, '', border='B', ln=1)
            pdf.ln(5)
            
            # Academic summary
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(*primary_color)
            pdf.cell(0, 8, "ACADEMIC SUMMARY", ln=1)
            pdf.ln(2)
            
            pdf.set_font('Helvetica', '', 11)
            pdf.set_text_color(*text_color)
            
            # Summary data
            summary_data = [
                ("Total Credits:", self.total_credits_label.cget("text")),
                ("Total Grade Points:", self.total_points_label.cget("text")),
                ("GPA:", self.gpa_label.cget("text")),
                ("Academic Standing:", self.standing_label.cget("text"))
            ]
            
            for label, value in summary_data:
                pdf.cell(60, 8, label)
                pdf.set_font('Helvetica', 'B', 11)
                pdf.cell(0, 8, value, ln=1)
                pdf.set_font('Helvetica', '', 11)
            
            pdf.ln(10)
            
            # Footer
            today = datetime.date.today().strftime("%B %d, %Y")
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 5, f"Generated on: {today}", ln=1, align='C')
            pdf.cell(0, 5, "This is an official document issued by the University Registrar", 
                    ln=1, align='C')
            
            # Save PDF
            pdf.output(filename)
            
            self.status_var.set(f"Transcript exported to PDF")
            messagebox.showinfo("Export Successful", 
                              f"Transcript has been exported to {os.path.abspath(filename)}")
            
        except Exception as e:
            messagebox.showerror("PDF Export Error", f"Failed to create PDF: {str(e)}")
            self.status_var.set("PDF export failed")

if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicTranscriptGenerator(root)
    root.mainloop()