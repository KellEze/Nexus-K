#!/usr/bin/env python3
"""
show_nexus.py
Small tkinter app to display Nexus Infinity interview and production-sector report.
Run: python3 show_nexus.py
"""
import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import messagebox  

COMPANY_INFO = {
    "name": "Nexus Infinity",
    "area": "Jogos e brinquedos",
    "product": "Fazer brinquedos e jogos com produtos recicláveis, criando jogos envolventes e inovadores que proporcionem experiências únicas, despertem emoções e conectem pessoas, transformando ideias em diversão e qualidade.",
    "audience": "Pessoas acima dos oito anos",
    "brief": (
        "Nexus Infinity quer reunir jogos, reciclagem e valores. Missão: criar brinquedos e jogos recicláveis que ofereçam experiências únicas,\n"
        "despertem emoções e conectem pessoas. Visão: ser referência global em criatividade, qualidade e impacto positivo."
    )
}

MARKETING_REPORT = {
    "owner": "Thomas (dono)",
    "manager": "Arthur (gerente do marketing)",
    "submanager": "Maria (subgerente)",
    "company": "Nexus Infinity",
    "area": "Marketing",
    "product": "Fazer brinquedos e jogos com produtos recicláveis",
    "audience": "Pessoas de todas as idades",
    "description": (
        "Compreender a visão do proprietário sobre o funcionamento da empresa, a eficiência dos setores,\n"
        "os desafios enfrentados e as perspectivas futuras do negócio."
    )
}

MARKETING_HELP = (
    "Função geral do Marketing:\n"
    "- Desenvolver identidade visual e designs dos brinquedos e materiais de divulgação.\n"
    "- Divulgar a empresa e atrair clientes; auxiliar na apresentação do produto.\n"
    "Problema citado por Ellen: Atraso na entrega dos designs, que atrasou a Produção.\n"
    'Comentário de Ellen: "Eu tive um pouco de problema com o Marketing porque eles não estavam entregando o design no prazo."'
)

HISTORY_ROWS = [
    ("22/06/2026", "Marketing", "Análise das redes sociais da empresa"),
    ("22/06/2026", "Financeiro", "Levantamento dos possíveis custos"),
    ("22/06/2026", "Produção", "Estudo do processo de entrega do produto"),
    ("22/06/2026", "RH", "Análise da organização das funções")
]

INTERVIEWERS = ("Maria de Alencar", "Amanda")


def make_label(frame, text, **kwargs):
    lbl = tk.Label(frame, text=text, justify=tk.LEFT, anchor='w', **kwargs)
    return lbl


def show_interviewers(root):
    w = tk.Toplevel(root)
    w.title("Entrevistadores - Nexus Infinity")
    w.geometry("700x400")

    header = tk.Frame(w)
    header.pack(fill='x', padx=12, pady=8)
    tk.Label(header, text=COMPANY_INFO['name'], font=(None, 20, 'bold')).pack(anchor='w')
    tk.Label(header, text=f"Entrevistadores: {', '.join(INTERVIEWERS)}", font=(None, 12)).pack(anchor='w')

    body = tk.Frame(w)
    body.pack(fill='both', expand=True, padx=12, pady=6)
    txt = tk.Text(body, wrap='word', height=12)
    txt.insert('end', f"Área de atuação: {COMPANY_INFO['area']}\n\n")
    txt.insert('end', f"Produto/serviço principal: {COMPANY_INFO['product']}\n\n")
    txt.insert('end', f"Público-alvo: {COMPANY_INFO['audience']}\n\n")
    txt.insert('end', f"Descrição: {COMPANY_INFO['brief']}\n")
    txt.configure(state='disabled')
    txt.pack(fill='both', expand=True)


def show_diario_marketing(root):
    w = tk.Toplevel(root)
    w.title("Diário de Entrevistados - Marketing")
    w.geometry("1050x720")

    notes_file = os.path.join(os.path.dirname(__file__), 'marketing_diario.json')

    def _empty_entry():
        return {
            'date': '',
            'interviewer': '',
            'summary': '',
            'interview': '',
            'observations': ''
        }

    entries = []
    selected_index = None

    # Header
    header = tk.Frame(w)
    header.pack(fill='x', padx=12, pady=8)
    tk.Label(header, text='Diário de Entrevistados (Marketing)', font=(None, 18, 'bold')).pack(anchor='w')
    tk.Label(header, text=f"{COMPANY_INFO['name']} • Salvo em marketing_diario.json", font=(None, 10), fg='gray').pack(anchor='w')

    # Controls row
    controls = tk.Frame(w)
    controls.pack(fill='x', padx=12, pady=(0,8))

    def set_status(msg: str):
        status_label.config(text=msg)

    btns = tk.Frame(controls)
    btns.pack(side='left')

    def new_entry():
        nonlocal selected_index, entries
        selected_index = None
        entry_date_var.set('')
        interviewer_var.set(INTERVIEWERS[0] if INTERVIEWERS else '')
        summary_var.set('')
        interview_text.delete('1.0', 'end')
        observations_text.delete('1.0', 'end')
        set_status('Criando nova entrada...')

    def load_entries():
        nonlocal entries, selected_index
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                entries = data.get('entries', []) if isinstance(data, dict) else []
                if not isinstance(entries, list):
                    entries = []
            except Exception as e:
                messagebox.showwarning('Erro', f'Erro ao carregar o diário: {e}')
                entries = []
        else:
            entries = []

        # refresh tree
        for item in tree.get_children():
            tree.delete(item)
        for i, ent in enumerate(entries):
            tree.insert('', 'end', iid=str(i), values=(
                ent.get('date', ''),
                ent.get('interviewer', ''),
                ent.get('summary', '')
            ))

        selected_index = None
        new_entry()
        set_status(f'{len(entries)} entrada(s) carregada(s).')

    def save_entries():
        nonlocal entries, selected_index
        # Build from UI
        current = {
            'date': entry_date_var.get().strip(),
            'interviewer': interviewer_var.get().strip(),
            'summary': summary_var.get().strip(),
            'interview': interview_text.get('1.0', 'end').strip(),
            'observations': observations_text.get('1.0', 'end').strip()
        }

        if not current['date']:
            messagebox.showwarning('Validação', 'Informe a data da entrevista.')
            return
        if not current['interviewer']:
            messagebox.showwarning('Validação', 'Informe o entrevistador.')
            return

        if selected_index is None:
            entries.append(current)
            selected_index = len(entries) - 1
        else:
            # ensure bounds
            if selected_index < 0 or selected_index >= len(entries):
                entries = entries[:]
                entries.append(current)
                selected_index = len(entries) - 1
            else:
                entries[selected_index] = current

        try:
            with open(notes_file, 'w', encoding='utf-8') as f:
                json.dump({'entries': entries}, f, ensure_ascii=False, indent=2)
            set_status('Salvo com sucesso.')

            # refresh tree row (simple full refresh to keep iid consistent)
            for item in tree.get_children():
                tree.delete(item)
            for i, ent in enumerate(entries):
                tree.insert('', 'end', iid=str(i), values=(
                    ent.get('date', ''),
                    ent.get('interviewer', ''),
                    ent.get('summary', '')
                ))

            # reselect
            if selected_index is not None and 0 <= selected_index < len(entries):
                tree.selection_set(str(selected_index))
                tree.focus(str(selected_index))
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao salvar: {e}')

    def delete_entry():
        nonlocal entries, selected_index
        if selected_index is None:
            messagebox.showinfo('Excluir', 'Selecione uma entrada para excluir.')
            return
        if selected_index < 0 or selected_index >= len(entries):
            selected_index = None
            return

        if not messagebox.askyesno('Excluir', 'Excluir esta entrada do diário?'):
            return

        entries.pop(selected_index)
        selected_index = None
        load_entries()
        set_status('Entrada excluída.')

    btn_new = tk.Button(btns, text='Nova entrada', width=14, command=new_entry)
    btn_load = tk.Button(btns, text='Carregar', width=10, command=load_entries)
    btn_save = tk.Button(btns, text='Salvar', width=10, command=save_entries)
    btn_del = tk.Button(btns, text='Excluir', width=10, command=delete_entry)

    btn_new.grid(row=0, column=0, padx=4)
    btn_load.grid(row=0, column=1, padx=4)
    btn_save.grid(row=0, column=2, padx=4)
    btn_del.grid(row=0, column=3, padx=4)

    status_label = tk.Label(controls, text='', fg='gray')
    status_label.pack(side='right')

    # Main split
    split = tk.Frame(w)
    split.pack(fill='both', expand=True, padx=12, pady=6)

    left = tk.Frame(split)
    left.pack(side='left', fill='y', padx=(0,10))

    tree_frame = tk.LabelFrame(left, text='Entradas')
    tree_frame.pack(fill='y', padx=0, pady=0)

    cols = ('date', 'interviewer', 'summary')
    tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=18)
    tree.heading('date', text='Data')
    tree.heading('interviewer', text='Entrevistador')
    tree.heading('summary', text='Resumo')
    tree.column('date', width=90)
    tree.column('interviewer', width=130)
    tree.column('summary', width=300)
    tree.pack(fill='y', padx=6, pady=6)

    def on_select(_evt=None):
        nonlocal selected_index
        sel = tree.selection()
        if not sel:
            selected_index = None
            return
        idx = int(sel[0])
        if idx < 0 or idx >= len(entries):
            return
        selected_index = idx

        ent = entries[idx]
        entry_date_var.set(ent.get('date', ''))
        interviewer_var.set(ent.get('interviewer', '') or (INTERVIEWERS[0] if INTERVIEWERS else ''))
        summary_var.set(ent.get('summary', ''))

        interview_text.delete('1.0', 'end')
        interview_text.insert('end', ent.get('interview', ''))

        observations_text.delete('1.0', 'end')
        observations_text.insert('end', ent.get('observations', ''))
        set_status('Entrada selecionada. Ajuste e clique em Salvar.')

    tree.bind('<<TreeviewSelect>>', on_select)

    right = tk.Frame(split)
    right.pack(side='left', fill='both', expand=True)

    details = tk.LabelFrame(right, text='Detalhes (entrevista e observações)')
    details.pack(fill='both', expand=True, padx=0, pady=0)

    top_form = tk.Frame(details)
    top_form.pack(fill='x', padx=10, pady=8)

    tk.Label(top_form, text='Data (dd/mm/aaaa):').grid(row=0, column=0, sticky='w')
    entry_date_var = tk.StringVar()
    tk.Entry(top_form, textvariable=entry_date_var, width=14).grid(row=0, column=1, sticky='w', padx=(6,16))

    tk.Label(top_form, text='Entrevistador:').grid(row=0, column=2, sticky='w')
    interviewer_var = tk.StringVar(value=(INTERVIEWERS[0] if INTERVIEWERS else ''))
    interviewer_combo = ttk.Combobox(top_form, textvariable=interviewer_var, values=list(INTERVIEWERS), state='readonly', width=22)
    interviewer_combo.grid(row=0, column=3, sticky='w', padx=(6,16))

    tk.Label(top_form, text='Resumo:').grid(row=1, column=0, sticky='w', pady=(8,0))
    summary_var = tk.StringVar()
    tk.Entry(top_form, textvariable=summary_var).grid(row=1, column=1, columnspan=3, sticky='we', padx=(6,0), pady=(8,0))
    top_form.grid_columnconfigure(1, weight=1)
    top_form.grid_columnconfigure(3, weight=1)

    mid = tk.Frame(details)
    mid.pack(fill='both', expand=True, padx=10, pady=10)

    left_mid = tk.Frame(mid)
    left_mid.pack(side='left', fill='both', expand=True, padx=(0,6))

    tk.Label(left_mid, text='Entrevista:').pack(anchor='w')
    interview_text = tk.Text(left_mid, wrap='word', height=12)
    interview_text.pack(fill='both', expand=True, pady=(4,0))

    right_mid = tk.Frame(mid)
    right_mid.pack(side='left', fill='both', expand=True, padx=(6,0))

    tk.Label(right_mid, text='Observações:').pack(anchor='w')
    observations_text = tk.Text(right_mid, wrap='word', height=12)
    observations_text.pack(fill='both', expand=True, pady=(4,0))

    # Bottom helper
    hint = tk.Label(details, text='Dica: selecione uma entrada na lista para editar. Ao salvar, o JSON é atualizado.', fg='gray')
    hint.pack(anchor='w', padx=10, pady=(0,10))

    # initial load
    load_entries()


def show_marketing_report(root):
    w = tk.Toplevel(root)
    w.title("Relatório - Setor de Marketing")
    w.geometry("900x700")


    header = tk.Frame(w)
    header.pack(fill='x', padx=12, pady=8)
    tk.Label(header, text=f"Relatório do Setor de Marketing - {MARKETING_REPORT['company']}", font=(None, 18, 'bold')).pack(anchor='w')

    info = tk.Frame(w)
    info.pack(fill='x', padx=12, pady=6)
    make_label(info, f"Dono da empresa: {MARKETING_REPORT['owner']}", font=(None, 11)).pack(anchor='w')
    make_label(info, f"Gerente do Marketing: {MARKETING_REPORT['manager']}", font=(None, 11)).pack(anchor='w')
    make_label(info, f"Subgerente: {MARKETING_REPORT['submanager']}", font=(None, 11)).pack(anchor='w')
    make_label(info, f"Área: {MARKETING_REPORT['area']}", font=(None, 11)).pack(anchor='w')
    make_label(info, f"Produto/serviço principal: {MARKETING_REPORT['product']}", font=(None, 11)).pack(anchor='w')
    make_label(info, f"Público-alvo: {MARKETING_REPORT['audience']}", font=(None, 11)).pack(anchor='w')

    desc_frame = tk.LabelFrame(w, text='Breve descrição')
    desc_frame.pack(fill='both', expand=False, padx=12, pady=8)
    tk.Label(desc_frame, text=MARKETING_REPORT['description'], justify='left', wraplength=840).pack(anchor='w', padx=6, pady=6)

    # Notes area: entrevista e observações (editáveis)
    notes_frame = tk.LabelFrame(w, text='Entrevista e Observações (edite abaixo)')
    notes_frame.pack(fill='both', expand=True, padx=12, pady=8)

    left = tk.Frame(notes_frame)
    left.pack(side='left', fill='both', expand=True, padx=(6,3), pady=6)
    tk.Label(left, text='Entrevista realizada (quem entrevistou: Maria de Alencar, Amanda):', anchor='w', justify='left').pack(anchor='w')
    interview_text = tk.Text(left, wrap='word', height=10)
    interview_text.pack(fill='both', expand=True, pady=(4,6))

    right = tk.Frame(notes_frame)
    right.pack(side='right', fill='both', expand=True, padx=(3,6), pady=6)
    tk.Label(right, text='Observações sobre o Marketing:', anchor='w', justify='left').pack(anchor='w')
    observations_text = tk.Text(right, wrap='word', height=10)
    observations_text.pack(fill='both', expand=True, pady=(4,6))

    # helper functions to save/load notes to a local JSON file
    notes_file = os.path.join(os.path.dirname(__file__), 'marketing_notes.json')

    def load_notes():
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                interview_text.delete('1.0', 'end')
                observations_text.delete('1.0', 'end')
                interview_text.insert('end', data.get('interview', ''))
                observations_text.insert('end', data.get('observations', ''))
            except Exception as e:
                messagebox.showwarning('Erro', f'Erro ao carregar notas: {e}')

    def save_notes():
        data = {
            'interview': interview_text.get('1.0', 'end').strip(),
            'observations': observations_text.get('1.0', 'end').strip()
        }
        try:
            with open(notes_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo('Salvo', f'Notas salvas em: {notes_file}')
            update_saved_display()
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao salvar: {e}')

    btns = tk.Frame(w)
    btns.pack(fill='x', padx=12, pady=(0,8))
    tk.Button(btns, text='Carregar notas existentes', command=load_notes, width=20).pack(side='left', padx=6)
    tk.Button(btns, text='Salvar notas', command=save_notes, width=14).pack(side='left', padx=6)
    tk.Button(btns, text='Abrir Diário de Entrevistados (Marketing)', command=lambda: show_diario_marketing(w), width=34).pack(side='left', padx=10)

    # Display saved notes below for quick review

    saved_frame = tk.LabelFrame(w, text='Notas salvas (visualização)')
    saved_frame.pack(fill='both', expand=False, padx=12, pady=6)
    saved_label = tk.Label(saved_frame, text='', justify='left', anchor='w', wraplength=840)
    saved_label.pack(fill='both', expand=True, padx=6, pady=6)

    def update_saved_display():
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                text = f"Entrevista:\n{data.get('interview','')}\n\nObservações:\n{data.get('observations','')}"
                saved_label.config(text=text)
            except Exception as e:
                saved_label.config(text=f'Erro ao ler arquivo: {e}')
        else:
            saved_label.config(text='Nenhuma nota salva ainda.')

    # load any existing notes on opening
    load_notes()
    update_saved_display()

    # histórico e conclusão (mantidos)
    hist_frame = tk.LabelFrame(w, text='Histórico da análise')
    hist_frame.pack(fill='both', expand=True, padx=12, pady=8)

    cols = ('date', 'sector', 'desc')
    tree = ttk.Treeview(hist_frame, columns=cols, show='headings', height=6)
    tree.heading('date', text='Data')
    tree.heading('sector', text='Setor')
    tree.heading('desc', text='Descrição')
    tree.column('date', width=100)
    tree.column('sector', width=120)
    tree.column('desc', width=520)
    for r in HISTORY_ROWS:
        tree.insert('', 'end', values=r)
    tree.pack(fill='both', expand=True, padx=6, pady=6)

    concl_frame = tk.LabelFrame(w, text='Conclusão da equipe')
    concl_frame.pack(fill='both', expand=False, padx=12, pady=8)
    conclusion = (
        "Concluímos que o setor de Marketing é essencial para divulgar e posicionar os produtos.\n"
        "Principal problema observado: atrasos na entrega dos designs, que impactam Produção.\n"
        "Melhoria prioritária: melhorar o cronograma entre Marketing e Produção, e criar checklists para entrega de designs."
    )
    tk.Label(concl_frame, text=conclusion, justify='left', wraplength=840).pack(anchor='w', padx=6, pady=6)


def main():
    root = tk.Tk()
    root.title('Nexus Infinity - Painel')
    root.geometry('640x320')

    style = ttk.Style()
    try:
        style.theme_use('clam')
    except Exception:
        pass

    header = tk.Frame(root)
    header.pack(fill='x', pady=(12,6))
    tk.Label(header, text='Nexus Infinity', font=(None, 22, 'bold')).pack()
    tk.Label(header, text=f"Entrevistadores: {', '.join(INTERVIEWERS)}", font=(None, 10)).pack()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=18)
    tk.Button(btn_frame, text='Mostrar entrevistadores e apresentação', width=36, command=lambda: show_interviewers(root)).grid(row=0, column=0, padx=8, pady=6)
    tk.Button(btn_frame, text='Relatório do Setor de Marketing', width=36, command=lambda: show_marketing_report(root)).grid(row=1, column=0, padx=8, pady=6)


    footer = tk.Frame(root)
    footer.pack(side='bottom', fill='x', pady=8)
    tk.Label(footer, text='Clique em Relatório do Setor de Marketing para abrir a tela com edição de entrevistas e observações.', font=(None, 9), fg='gray').pack()

    root.mainloop()

if __name__ == '__main__':
    main()
