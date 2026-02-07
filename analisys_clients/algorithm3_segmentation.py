import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import random
import csv
import matplotlib

# Указываем бэкенд для matplotlib
matplotlib.use('TkAgg')


class RFMSegmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм 3: RFM-сегментация клиентов")
        self.root.geometry("1200x800")

        self.center_window()
        self.create_demo_database()
        self.conn = sqlite3.connect("segmentation.db")
        self.cursor = self.conn.cursor()

        self.setup_styles()
        self.create_widgets()
        self.perform_segmentation()

    def center_window(self):
        self.root.update_idletasks()
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('VIP.TLabel', font=('Arial', 10, 'bold'), foreground='#b8860b')
        style.configure('Blue.TButton', background='#3498db', foreground='white')
        style.configure('Green.TButton', background='#2ecc71', foreground='white')
        style.configure('Red.TButton', background='#e74c3c', foreground='white')

    def create_demo_database(self):
        """Создание демо-базы с клиентами и покупками"""
        conn = sqlite3.connect("segmentation.db")
        cursor = conn.cursor()

        # Таблица клиентов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            registration_date DATE
        )
        ''')

        # Таблица заказов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        ''')

        # Проверяем и добавляем демо-данные
        cursor.execute("SELECT COUNT(*) FROM customers")
        if cursor.fetchone()[0] == 0:
            # Создаем 150 клиентов
            names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов",
                     "Попов", "Лебедев", "Козлов", "Новиков", "Морозов"]

            current_id = 1
            today = datetime.now()

            # 6 типов клиентов для демонстрации RFM
            customer_types = [
                ("VIP", 15, 50000, 12),  # Часто покупают, недавно, много тратят
                ("Постоянные", 45, 25000, 8),  # Часто покупают, но подешевле
                ("Новые", 5, 10000, 2),  # Недавно зарегистрировались
                ("Уходящие", 180, 5000, 1),  # Давно не покупали
                ("Спящие", 400, 2000, 0),  # Очень давно не покупали
                ("Обычные", 90, 15000, 4)  # Средние по всем параметрам
            ]

            for ctype, recency_days, avg_amount, order_count in customer_types:
                for i in range(25):  # По 25 клиентов каждого типа
                    name = f"{names[current_id % 10]} {current_id}"
                    email = f"client{current_id}@mail.com"

                    # Дата регистрации от 1 до 3 лет назад
                    reg_date = today - timedelta(days=random.randint(365, 1095))

                    cursor.execute(
                        "INSERT INTO customers (customer_id, name, email, registration_date) VALUES (?, ?, ?, ?)",
                        (current_id, name, email, reg_date.date())
                    )

                    # Добавляем заказы
                    for order_num in range(order_count):
                        order_date = today - timedelta(days=recency_days + random.randint(-30, 30))
                        amount = avg_amount + random.randint(-5000, 5000)

                        cursor.execute(
                            "INSERT INTO orders (customer_id, order_date, amount) VALUES (?, ?, ?)",
                            (current_id, order_date.date(), max(amount, 1000))
                        )

                    current_id += 1

            print(f"✅ Создано {current_id - 1} демо-клиентов с разными RFM-профилями")

        conn.commit()
        conn.close()

    def create_widgets(self):
        """Создание интерфейса"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="🎯 RFM-СЕГМЕНТАЦИЯ КЛИЕНТОВ (Recency-Frequency-Monetary)",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 15))

        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 15))

        buttons = [
            ("🔄 Выполнить сегментацию", self.perform_segmentation, "Blue.TButton"),
            ("📊 Диаграмма сегментов", self.show_segments_chart, "Blue.TButton"),
            ("👑 VIP Клиенты", self.show_vip_clients, "Green.TButton"),
            ("📈 ТОП-20 клиентов", self.show_top_clients, "Green.TButton"),
            ("📋 Экспорт данных", self.export_data, "Red.TButton"),
            ("🧹 Очистить таблицу", self.clear_table, ""),
            ("ℹ️ Что такое RFM?", self.show_rfm_info, "")
        ]

        for text, command, style in buttons:
            if style:
                btn = ttk.Button(control_frame, text=text, command=command, style=style)
            else:
                btn = ttk.Button(control_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5)

        # Панель с сегментами
        segments_frame = ttk.LabelFrame(main_frame, text="Сегменты клиентов", padding="10")
        segments_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Создаем фреймы для каждого сегмента
        self.create_segment_boxes(segments_frame)

        # Детальная таблица
        table_frame = ttk.LabelFrame(main_frame, text="Детальная информация по клиентам", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.create_detail_table(table_frame)

    def create_segment_boxes(self, parent):
        """Создание визуальных блоков для каждого сегмента"""
        segments_frame = ttk.Frame(parent)
        segments_frame.pack(fill=tk.BOTH, expand=True)

        # Определяем сегменты и их цвета
        self.segments = {
            "VIP Клиенты": {"color": "#FFD700", "desc": "Покупают часто, недавно и много"},
            "Постоянные": {"color": "#90EE90", "desc": "Покупают регулярно, но меньше"},
            "Новые": {"color": "#87CEEB", "desc": "Недавно начали покупать"},
            "Уходящие": {"color": "#FFA07A", "desc": "Давно не покупали, но были активны"},
            "Спящие": {"color": "#D3D3D3", "desc": "Очень давно не покупали"},
            "Обычные": {"color": "#FFFFFF", "desc": "Все остальные клиенты"}
        }

        self.segment_vars = {}

        # Создаем по 2 сегмента в строке
        row_frame = None
        for idx, (name, info) in enumerate(self.segments.items()):
            if idx % 2 == 0:
                row_frame = ttk.Frame(segments_frame)
                row_frame.pack(fill=tk.X, pady=5)

            seg_frame = ttk.LabelFrame(row_frame, text=name, padding="10")
            seg_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

            # Статистика сегмента
            stats_label = ttk.Label(
                seg_frame,
                text="Загрузка...",
                font=('Arial', 11, 'bold'),
                foreground='black'
            )
            stats_label.pack(pady=5)

            desc_label = ttk.Label(
                seg_frame,
                text=info['desc'],
                font=('Arial', 9),
                wraplength=200
            )
            desc_label.pack()

            # Сохраняем ссылку на label для обновления
            self.segment_vars[name] = stats_label

            # Устанавливаем цвет фона
            seg_frame.configure(style='TLabelframe')

    def create_detail_table(self, parent):
        """Создание таблицы с детальной информацией"""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Имя", "R (дней)", "F", "M (₽)", "RFM Счет", "Сегмент", "Рекомендация")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        column_widths = [50, 150, 80, 50, 100, 80, 120, 200]
        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def perform_segmentation(self):
        """Выполнение RFM-анализа"""
        try:
            # SQL-запрос для RFM-анализа
            query = """
            WITH customer_stats AS (
                SELECT 
                    c.customer_id,
                    c.name,
                    -- Recency: сколько дней назад была последняя покупка
                    COALESCE(MAX(o.order_date), c.registration_date) as last_date,
                    -- Frequency: сколько было заказов за последний год
                    COUNT(o.order_id) as order_count,
                    -- Monetary: общая сумма покупок
                    COALESCE(SUM(o.amount), 0) as total_amount
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
            ),
            rfm_raw AS (
                SELECT *,
                    -- Расчет дней с последней покупки
                    JULIANDAY('now') - JULIANDAY(last_date) as recency_days
                FROM customer_stats
            ),
            rfm_scores AS (
                SELECT *,
                    -- Оценка Recency (чем меньше дней - тем лучше)
                    CASE 
                        WHEN recency_days <= 30 THEN 5
                        WHEN recency_days <= 60 THEN 4
                        WHEN recency_days <= 120 THEN 3
                        WHEN recency_days <= 365 THEN 2
                        ELSE 1
                    END as R,
                    -- Оценка Frequency
                    CASE 
                        WHEN order_count >= 10 THEN 5
                        WHEN order_count >= 5 THEN 4
                        WHEN order_count >= 3 THEN 3
                        WHEN order_count >= 1 THEN 2
                        ELSE 1
                    END as F,
                    -- Оценка Monetary
                    CASE 
                        WHEN total_amount >= 100000 THEN 5
                        WHEN total_amount >= 50000 THEN 4
                        WHEN total_amount >= 20000 THEN 3
                        WHEN total_amount >= 5000 THEN 2
                        ELSE 1
                    END as M
                FROM rfm_raw
            )
            SELECT 
                customer_id,
                name,
                ROUND(recency_days) as R_days,
                order_count as F_count,
                ROUND(total_amount) as M_total,
                R,
                F,
                M,
                (R + F + M) as RFM_score,
                CASE
                    WHEN R >= 4 AND F >= 4 AND M >= 4 THEN 'VIP Клиенты'
                    WHEN F >= 4 AND M >= 3 THEN 'Постоянные'
                    WHEN R >= 4 AND order_count <= 3 THEN 'Новые'
                    WHEN R = 1 AND F <= 2 THEN 'Уходящие'
                    WHEN R <= 2 AND F <= 2 AND M <= 2 THEN 'Спящие'
                    ELSE 'Обычные'
                END as segment,
                CASE
                    WHEN R >= 4 AND F >= 4 AND M >= 4 THEN 'Персональный менеджер, эксклюзивные предложения'
                    WHEN F >= 4 AND M >= 3 THEN 'Программа лояльности, скидки 15%'
                    WHEN R >= 4 AND order_count <= 3 THEN 'Приветственный бонус, обучение'
                    WHEN R = 1 AND F <= 2 THEN 'Спецпредложение для возврата'
                    WHEN R <= 2 AND F <= 2 AND M <= 2 THEN 'Напоминание, опрос причин'
                    ELSE 'Регулярные рассылки, общие акции'
                END as recommendation
            FROM rfm_scores
            ORDER BY RFM_score DESC
            """

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                messagebox.showwarning("Нет данных", "В базе данных нет клиентов для анализа")
                return

            # Очищаем таблицу
            self.clear_table()

            # Заполняем таблицу (первые 50 клиентов для наглядности)
            for row in results[:50]:
                formatted_row = (
                    row[0],  # ID
                    row[1],  # Имя
                    row[2],  # R (дней)
                    row[3],  # F
                    f"{row[4]:,} ₽".replace(",", " "),  # M (₽)
                    f"{row[8]}/15",  # RFM Счет
                    row[9],  # Сегмент
                    row[10]  # Рекомендация
                )
                self.tree.insert("", "end", values=formatted_row)

            # Обновляем статистику по сегментам
            self.update_segment_stats(results)

            # Показываем общую статистику
            total_clients = len(results)
            vip_count = sum(1 for row in results if row[9] == 'VIP Клиенты')
            avg_score = sum(row[8] for row in results) / total_clients if total_clients > 0 else 0

            # Статистика в заголовке
            stats_text = f"RFM-анализ: {total_clients} клиентов | VIP: {vip_count} | Средний счет: {avg_score:.1f}/15"
            self.root.title(f"Алгоритм 3: RFM-сегментация клиентов - {stats_text}")

            messagebox.showinfo(
                "RFM-анализ завершен",
                f"✅ Проанализировано клиентов: {total_clients}\n"
                f"VIP клиентов: {vip_count}\n"
                f"Средний RFM-счет: {avg_score:.1f}/15\n\n"
                f"Данные загружены в таблицу."
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить сегментацию:\n{str(e)}")

    def update_segment_stats(self, data):
        """Обновление статистики по сегментам"""
        try:
            # Считаем клиентов по сегментам
            segment_counts = {}
            segment_revenue = {}

            for row in data:
                segment = row[9]  # Название сегмента
                revenue = row[4]  # Сумма покупок

                if segment not in segment_counts:
                    segment_counts[segment] = 0
                    segment_revenue[segment] = 0

                segment_counts[segment] += 1
                segment_revenue[segment] += revenue

            # Обновляем labels
            total_clients = len(data)

            for segment_name, label in self.segment_vars.items():
                count = segment_counts.get(segment_name, 0)
                revenue = segment_revenue.get(segment_name, 0)

                if count > 0:
                    percentage = (count / total_clients) * 100
                    avg_revenue = revenue / count if count > 0 else 0
                    label.config(
                        text=f"{count} клиентов ({percentage:.1f}%)\n"
                             f"Средний доход: {avg_revenue:,.0f} ₽"
                    )
                else:
                    label.config(text=f"0 клиентов (0%)\nНет данных")

        except Exception as e:
            print(f"Ошибка при обновлении статистики: {e}")

    def clear_table(self):
        """Очистка таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def show_segments_chart(self):
        """Показать круговую диаграмму сегментов"""
        try:
            # Получаем данные о сегментах
            query = """
            WITH rfm_scores AS (
                SELECT 
                    c.customer_id,
                    COALESCE(MAX(o.order_date), c.registration_date) as last_date,
                    COUNT(o.order_id) as order_count,
                    COALESCE(SUM(o.amount), 0) as total_amount,
                    JULIANDAY('now') - JULIANDAY(COALESCE(MAX(o.order_date), c.registration_date)) as recency_days
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
            ),
            rfm_calculated AS (
                SELECT *,
                    CASE 
                        WHEN recency_days <= 30 THEN 5
                        WHEN recency_days <= 60 THEN 4
                        WHEN recency_days <= 120 THEN 3
                        WHEN recency_days <= 365 THEN 2
                        ELSE 1
                    END as R,
                    CASE 
                        WHEN order_count >= 10 THEN 5
                        WHEN order_count >= 5 THEN 4
                        WHEN order_count >= 3 THEN 3
                        WHEN order_count >= 1 THEN 2
                        ELSE 1
                    END as F,
                    CASE 
                        WHEN total_amount >= 100000 THEN 5
                        WHEN total_amount >= 50000 THEN 4
                        WHEN total_amount >= 20000 THEN 3
                        WHEN total_amount >= 5000 THEN 2
                        ELSE 1
                    END as M
                FROM rfm_scores
            )
            SELECT 
                CASE
                    WHEN R >= 4 AND F >= 4 AND M >= 4 THEN 'VIP Клиенты'
                    WHEN F >= 4 AND M >= 3 THEN 'Постоянные'
                    WHEN R >= 4 AND order_count <= 3 THEN 'Новые'
                    WHEN R = 1 AND F <= 2 THEN 'Уходящие'
                    WHEN R <= 2 AND F <= 2 AND M <= 2 THEN 'Спящие'
                    ELSE 'Обычные'
                END as segment,
                COUNT(*) as count
            FROM rfm_calculated
            GROUP BY segment
            ORDER BY count DESC
            """

            self.cursor.execute(query)
            segments_data = self.cursor.fetchall()

            if not segments_data:
                messagebox.showwarning("Нет данных", "Сначала выполните сегментацию!")
                return

            chart_window = tk.Toplevel(self.root)
            chart_window.title("Распределение клиентов по сегментам")
            chart_window.geometry("800x600")

            # Подготавливаем данные для диаграммы
            segments = [row[0] for row in segments_data]
            counts = [row[1] for row in segments_data]

            colors = ['#FFD700', '#90EE90', '#87CEEB', '#FFA07A', '#D3D3D3', '#A9A9A9']

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

            # Круговая диаграмма
            ax1.pie(counts, labels=segments, autopct='%1.1f%%',
                    colors=colors[:len(segments)], startangle=90, explode=[0.05] * len(segments))
            ax1.set_title('Распределение клиентов по сегментам', fontsize=14, fontweight='bold')

            # Столбчатая диаграмма
            bars = ax2.bar(segments, counts, color=colors[:len(segments)], edgecolor='black')
            ax2.set_title('Количество клиентов по сегментам', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Сегмент')
            ax2.set_ylabel('Количество клиентов')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3, axis='y')

            # Добавляем значения на столбцы
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                         f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Кнопки
            button_frame = ttk.Frame(chart_window)
            button_frame.pack(pady=10)

            ttk.Button(button_frame, text="Закрыть",
                       command=chart_window.destroy).pack(side=tk.LEFT, padx=5)

            ttk.Button(button_frame, text="💾 Сохранить график",
                       command=lambda: self.save_figure(fig, "rfm_segments")).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{str(e)}")

    def save_figure(self, fig, filename_prefix):
        """Сохранение графика в файл"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"

            fig.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Сохранено", f"График сохранен в файл:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить график:\n{str(e)}")

    def show_vip_clients(self):
        """Показать VIP клиентов"""
        try:
            query = """
            SELECT 
                c.name, 
                ROUND(COALESCE(SUM(o.amount), 0)) as total_amount,
                COUNT(o.order_id) as order_count,
                ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(MAX(o.order_date), c.registration_date))) as days_ago
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
            HAVING total_amount > 50000 AND order_count >= 5
            ORDER BY total_amount DESC
            LIMIT 20
            """

            self.cursor.execute(query)
            vip_clients = self.cursor.fetchall()

            if not vip_clients:
                messagebox.showinfo("VIP Клиенты", "VIP клиентов не найдено")
                return

            vip_window = tk.Toplevel(self.root)
            vip_window.title("VIP Клиенты - ТОП 20")
            vip_window.geometry("700x500")

            # Создаем таблицу
            columns = ("Имя", "Общая сумма (₽)", "Заказов", "Дней с последней покупки")
            tree = ttk.Treeview(vip_window, columns=columns, show="headings", height=15)

            col_widths = [200, 150, 100, 150]
            for col, width in zip(columns, col_widths):
                tree.heading(col, text=col)
                tree.column(col, width=width, anchor="center")

            for client in vip_clients:
                formatted_client = (
                    client[0],
                    f"{client[1]:,} ₽".replace(",", " "),
                    client[2],
                    f"{client[3]} дней"
                )
                tree.insert("", "end", values=formatted_client)

            scrollbar = ttk.Scrollbar(vip_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Статистика
            total_vip_revenue = sum(client[1] for client in vip_clients)
            avg_vip_revenue = total_vip_revenue / len(vip_clients) if vip_clients else 0

            stats_label = ttk.Label(
                vip_window,
                text=f"Всего VIP клиентов: {len(vip_clients)}\n"
                     f"Общая выручка от VIP: {total_vip_revenue:,.0f} ₽\n"
                     f"Средняя выручка на VIP: {avg_vip_revenue:,.0f} ₽",
                font=('Arial', 10, 'bold')
            )
            stats_label.pack(pady=5)

            ttk.Button(vip_window, text="Закрыть",
                       command=vip_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить VIP клиентов:\n{str(e)}")

    def show_top_clients(self):
        """Показать топ-20 клиентов по RFM-счету"""
        try:
            # Выполняем RFM-анализ для получения данных
            self.perform_segmentation()

            # Получаем всех клиентов из RFM-анализа
            query = """
            WITH rfm_scores AS (
                -- Тот же запрос что в perform_segmentation, но без лимита
                SELECT 
                    c.customer_id,
                    c.name,
                    JULIANDAY('now') - JULIANDAY(COALESCE(MAX(o.order_date), c.registration_date)) as recency_days,
                    COUNT(o.order_id) as order_count,
                    COALESCE(SUM(o.amount), 0) as total_amount
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
            ),
            rfm_calculated AS (
                SELECT *,
                    CASE 
                        WHEN recency_days <= 30 THEN 5
                        WHEN recency_days <= 60 THEN 4
                        WHEN recency_days <= 120 THEN 3
                        WHEN recency_days <= 365 THEN 2
                        ELSE 1
                    END as R,
                    CASE 
                        WHEN order_count >= 10 THEN 5
                        WHEN order_count >= 5 THEN 4
                        WHEN order_count >= 3 THEN 3
                        WHEN order_count >= 1 THEN 2
                        ELSE 1
                    END as F,
                    CASE 
                        WHEN total_amount >= 100000 THEN 5
                        WHEN total_amount >= 50000 THEN 4
                        WHEN total_amount >= 20000 THEN 3
                        WHEN total_amount >= 5000 THEN 2
                        ELSE 1
                    END as M
                FROM rfm_scores
            )
            SELECT 
                customer_id,
                name,
                ROUND(recency_days) as R_days,
                order_count as F_count,
                ROUND(total_amount) as M_total,
                (R + F + M) as RFM_score
            FROM rfm_calculated
            ORDER BY RFM_score DESC
            LIMIT 20
            """

            self.cursor.execute(query)
            top_clients = self.cursor.fetchall()

            if not top_clients:
                messagebox.showwarning("Нет данных", "Нет данных о клиентах")
                return

            top_window = tk.Toplevel(self.root)
            top_window.title("ТОП-20 клиентов по RFM-счету")
            top_window.geometry("800x500")

            columns = ("ID", "Имя", "R-дни", "F-заказы", "M-выручка (₽)", "RFM Счет")
            tree = ttk.Treeview(top_window, columns=columns, show="headings", height=15)

            col_widths = [50, 150, 80, 80, 150, 100]
            for col, width in zip(columns, col_widths):
                tree.heading(col, text=col)
                tree.column(col, width=width, anchor="center")

            for client in top_clients:
                formatted_client = (
                    client[0],
                    client[1],
                    client[2],
                    client[3],
                    f"{client[4]:,} ₽".replace(",", " "),
                    f"{client[5]}/15"
                )
                tree.insert("", "end", values=formatted_client)

            scrollbar = ttk.Scrollbar(top_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Статистика
            total_rfm = sum(client[5] for client in top_clients)
            avg_rfm = total_rfm / len(top_clients) if top_clients else 0

            stats_label = ttk.Label(
                top_window,
                text=f"Средний RFM-счет топ-20: {avg_rfm:.1f}/15 (максимум 15)\n"
                     f"Лучший счет: {max(client[5] for client in top_clients) if top_clients else 0}/15",
                font=('Arial', 10, 'bold')
            )
            stats_label.pack(pady=5)

            ttk.Button(top_window, text="Закрыть",
                       command=top_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить топ-клиентов:\n{str(e)}")

    def export_data(self):
        """Экспорт данных RFM-анализа в CSV"""
        try:
            # Выполняем RFM-анализ для получения данных
            self.perform_segmentation()

            # Получаем данные для экспорта
            query = """
            WITH rfm_scores AS (
                SELECT 
                    c.customer_id,
                    c.name,
                    JULIANDAY('now') - JULIANDAY(COALESCE(MAX(o.order_date), c.registration_date)) as recency_days,
                    COUNT(o.order_id) as order_count,
                    COALESCE(SUM(o.amount), 0) as total_amount
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
            ),
            rfm_calculated AS (
                SELECT *,
                    CASE 
                        WHEN recency_days <= 30 THEN 5
                        WHEN recency_days <= 60 THEN 4
                        WHEN recency_days <= 120 THEN 3
                        WHEN recency_days <= 365 THEN 2
                        ELSE 1
                    END as R,
                    CASE 
                        WHEN order_count >= 10 THEN 5
                        WHEN order_count >= 5 THEN 4
                        WHEN order_count >= 3 THEN 3
                        WHEN order_count >= 1 THEN 2
                        ELSE 1
                    END as F,
                    CASE 
                        WHEN total_amount >= 100000 THEN 5
                        WHEN total_amount >= 50000 THEN 4
                        WHEN total_amount >= 20000 THEN 3
                        WHEN total_amount >= 5000 THEN 2
                        ELSE 1
                    END as M
                FROM rfm_scores
            )
            SELECT 
                customer_id as ID,
                name as Имя,
                ROUND(recency_days) as 'Дней с последней покупки',
                order_count as 'Количество заказов',
                ROUND(total_amount) as 'Общая выручка',
                R as 'R-оценка',
                F as 'F-оценка',
                M as 'M-оценка',
                (R + F + M) as 'RFM-счет',
                CASE
                    WHEN R >= 4 AND F >= 4 AND M >= 4 THEN 'VIP Клиенты'
                    WHEN F >= 4 AND M >= 3 THEN 'Постоянные'
                    WHEN R >= 4 AND order_count <= 3 THEN 'Новые'
                    WHEN R = 1 AND F <= 2 THEN 'Уходящие'
                    WHEN R <= 2 AND F <= 2 AND M <= 2 THEN 'Спящие'
                    ELSE 'Обычные'
                END as 'Сегмент'
            FROM rfm_calculated
            ORDER BY (R + F + M) DESC
            """

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                messagebox.showwarning("Нет данных", "Нет данных для экспорта")
                return

            # Создаем имя файла с timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rfm_analysis_{timestamp}.csv"

            # Экспортируем в файл
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')

                # Записываем заголовки
                writer.writerow(['ID', 'Имя', 'Дней с последней покупки', 'Заказов',
                                 'Выручка (₽)', 'R', 'F', 'M', 'RFM-счет', 'Сегмент'])

                # Записываем данные
                for row in results:
                    writer.writerow(row)

            messagebox.showinfo("Экспорт завершен",
                                f"✅ Данные успешно экспортированы в файл:\n{filename}\n"
                                f"Всего клиентов: {len(results)}\n"
                                f"Формат: CSV с разделителем ';' (открывается в Excel)")

        except Exception as e:
            messagebox.showerror("Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")

    def show_rfm_info(self):
        """Показать информацию о RFM-анализе"""
        info_text = """
        🎯 ЧТО ТАКОЕ RFM-СЕГМЕНТАЦИЯ?

        RFM - это метод анализа клиентов по трем параметрам:

        1. RECENCY (давность) - R
           • Когда клиент последний раз покупал?
           • Чем меньше дней прошло - тем лучше оценка (1-5)
           • 5 баллов: покупал в последние 30 дней
           • 1 балл: не покупал больше года

        2. FREQUENCY (частота) - F  
           • Как часто клиент покупает?
           • Чем больше покупок - тем лучше оценка (1-5)
           • 5 баллов: 10+ заказов
           • 1 балл: 0 заказов

        3. MONETARY (деньги) - M
           • Сколько всего клиент потратил?
           • Чем больше сумма - тем лучше оценка (1-5)
           • 5 баллов: 100,000+ ₽
           • 1 балл: менее 5,000 ₽

        📊 КАК ИСПОЛЬЗОВАТЬ ЭТУ ПРОГРАММУ:

        1. ПРИ ЗАПУСКЕ программа автоматически:
           • Создает базу данных с демо-клиентами
           • Выполняет RFM-анализ
           • Показывает результаты

        2. КНОПКИ И ИХ ФУНКЦИИ:

           🔄 Выполнить сегментацию - основной анализ всех клиентов
           📊 Диаграмма сегментов - круговая и столбчатая диаграммы распределения
           👑 VIP Клиенты - список самых ценных клиентов (выручка > 50,000 ₽)
           📈 ТОП-20 клиентов - лучшие клиенты по RFM-счету (максимум 15 баллов)
           📋 Экспорт данных - сохраняет все данные RFM в CSV файл
           🧹 Очистить таблицу - очищает таблицу (данные остаются)
           ℹ️ Что такое RFM? - эта инструкция

        3. В ВЕРХНЕЙ ЧАСТИ экрана - 6 цветных блоков:
           • 🟨 VIP Клиенты - самые ценные (R≥4, F≥4, M≥4)
           • 🟩 Постоянные - регулярные покупатели (F≥4, M≥3)
           • 🟦 Новые - недавно начали покупать (R≥4, ≤3 заказов)
           • 🟧 Уходящие - давно не покупали (R=1, F≤2)
           • ⬜ Спящие - очень давно не покупали (R≤2, F≤2, M≤2)
           • ⬜ Обычные - все остальные клиенты

        4. В ТАБЛИЦЕ ВНИЗУ - детальная информация:
           • ID, Имя клиента
           • R (Recency) - дней с последней покупки
           • F (Frequency) - количество заказов
           • M (Monetary) - общая сумма покупок
           • RFM Счет - сумма R+F+M (3-15 баллов)
           • Сегмент - к какой группе относится
           • Рекомендация - что делать с этим клиентом

        5. 💡 СОВЕТЫ ПО ИСПОЛЬЗОВАНИЮ RFM:

           • VIP-клиентам: персональный менеджер, эксклюзивные предложения
           • Постоянным: программа лояльности, регулярные скидки
           • Новым: приветственный бонус, обучение использованию
           • Уходящим: спецпредложения для возврата, опрос причин ухода
           • Спящим: напоминания, реактивационные кампании
           • Обычным: регулярные рассылки, общие акции

        6. ⚠️ ВНИМАНИЕ:
           • Все данные генерируются автоматически при первом запуске
           • Для реальных данных замените функцию create_demo_database
           • RFM-счет от 3 до 15: 15 - идеальный клиент, 3 - самый плохой
        """

        info_window = tk.Toplevel(self.root)
        info_window.title("О RFM-анализе")
        info_window.geometry("800x600")

        text_widget = tk.Text(info_window, wrap="word", font=("Arial", 10))
        text_widget.insert("1.0", info_text)
        text_widget.config(state="disabled")

        scrollbar = ttk.Scrollbar(info_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(info_window, text="Закрыть",
                   command=info_window.destroy).pack(pady=10)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = RFMSegmentationApp(root)
    root.mainloop()