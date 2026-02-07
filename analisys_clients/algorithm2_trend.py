import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import random
import csv


class RegistrationTrendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм 2: Анализ динамики регистрации клиентов")
        self.root.geometry("1100x750")

        self.center_window()
        self.create_demo_database()
        self.conn = sqlite3.connect("trend_analysis.db")
        self.cursor = self.conn.cursor()

        self.setup_styles()
        self.create_widgets()
        self.update_chart()  # Автоматически загружаем данные при запуске

    def center_window(self):
        self.root.update_idletasks()
        width = 1100
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Red.TButton', background='#e74c3c', foreground='white')
        style.configure('Blue.TButton', background='#3498db', foreground='white')

    def create_demo_database(self):
        """Создание демо-базы с данными за 2 года"""
        conn = sqlite3.connect("trend_analysis.db")
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            registration_date DATE,
            source TEXT
        )
        ''')

        cursor.execute("SELECT COUNT(*) FROM clients")
        if cursor.fetchone()[0] == 0:
            # Создаем данные за 24 месяца (2 года)
            start_date = datetime.now() - timedelta(days=730)

            # Сезонность: больше клиентов весной и осенью
            season_factors = {
                1: 0.8, 2: 0.7, 3: 1.2, 4: 1.3, 5: 1.1, 6: 0.9,
                7: 0.8, 8: 0.7, 9: 1.4, 10: 1.5, 11: 1.2, 12: 1.0
            }

            sources = ['Сайт', 'Реклама', 'Рекомендации', 'Соцсети', 'Другое']

            client_id = 1

            # Генерируем клиентов на каждый месяц
            for month_offset in range(24):
                month_date = start_date + timedelta(days=30.44 * month_offset)
                month = month_date.month
                year = month_date.year

                # Базовое количество клиентов в месяц + сезонность + рост тренда
                base_clients = 30
                seasonal_factor = season_factors[month]
                trend_growth = 1 + (month_offset * 0.02)  # Постепенный рост

                month_clients = int(base_clients * seasonal_factor * trend_growth + random.randint(-5, 5))

                for i in range(month_clients):
                    name = f"Клиент_{client_id}"
                    email = f"client{client_id}@example.com"

                    # Случайная дата в пределах месяца
                    day_in_month = random.randint(1, 28)
                    reg_date = datetime(year, month, day_in_month).date()

                    source = random.choice(sources)

                    cursor.execute(
                        "INSERT INTO clients (name, email, registration_date, source) VALUES (?, ?, ?, ?)",
                        (name, email, reg_date, source)
                    )
                    client_id += 1

            print(f"✅ Создано {client_id - 1} демо-клиентов за 24 месяца")

        conn.commit()
        conn.close()

    def create_widgets(self):
        """Создание интерфейса"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="📈 АНАЛИЗ ДИНАМИКИ РЕГИСТРАЦИИ КЛИЕНТОВ",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 15))

        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Параметры анализа", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 15))

        # Выбор периода
        period_frame = ttk.Frame(control_frame)
        period_frame.pack(fill=tk.X, pady=5)

        ttk.Label(period_frame, text="Период анализа:").pack(side=tk.LEFT, padx=5)

        self.period_var = tk.StringVar(value="monthly")

        ttk.Radiobutton(period_frame, text="Помесячно",
                        variable=self.period_var, value="monthly").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(period_frame, text="Поквартально",
                        variable=self.period_var, value="quarterly").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(period_frame, text="Погодно",
                        variable=self.period_var, value="yearly").pack(side=tk.LEFT, padx=10)

        # Кнопки управления
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=10)

        buttons = [
            ("🔄 Обновить график", self.update_chart, "Blue.TButton"),
            ("📊 Столбчатая диаграмма", self.show_bar_chart, "Blue.TButton"),
            ("📈 Линейный график", self.show_line_chart, "Blue.TButton"),
            ("📉 Сравнить годы", self.compare_years, "Red.TButton"),
            ("📄 Экспорт данных", self.export_data, "Blue.TButton"),
            ("ℹ️ Справка", self.show_help, "")
        ]

        for text, command, style in buttons:
            if style:
                btn = ttk.Button(button_frame, text=text, command=command, style=style)
            else:
                btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5)

        # Основное окно для графиков
        self.chart_frame = ttk.Frame(main_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица с данными
        data_frame = ttk.LabelFrame(main_frame, text="Данные", padding="10")
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

        self.create_data_table(data_frame)

    def create_data_table(self, parent):
        """Создание таблицы для отображения данных"""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Период", "Новых клиентов", "Накопительный итог", "Рост %", "Тренд")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Статистика под таблицей
        self.stats_label = ttk.Label(parent, text="", font=('Arial', 10, 'bold'))
        self.stats_label.pack(pady=5)

    def load_data(self, period='monthly'):
        """Загрузка данных для анализа"""
        if period == 'monthly':
            date_format = "strftime('%Y-%m', registration_date)"
        elif period == 'quarterly':
            date_format = "strftime('%Y', registration_date) || '-Q' || ((strftime('%m', registration_date) + 2) / 3)"
        else:  # yearly
            date_format = "strftime('%Y', registration_date)"

        query = f"""
        SELECT 
            {date_format} as period,
            COUNT(*) as new_clients,
            SUM(COUNT(*)) OVER (ORDER BY {date_format}) as cumulative_total
        FROM clients
        WHERE registration_date IS NOT NULL
        GROUP BY period
        ORDER BY period
        """

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу
        prev_count = 0
        total_clients = 0
        max_growth = 0
        max_growth_period = ""
        min_growth = 0
        min_growth_period = ""

        for period, count, cumulative in data:
            total_clients = cumulative

            # Расчет роста
            if prev_count > 0:
                growth = ((count - prev_count) / prev_count * 100)
                if growth > max_growth:
                    max_growth = growth
                    max_growth_period = period
                if growth < min_growth:
                    min_growth = growth
                    min_growth_period = period
            else:
                growth = 0

            # Определение тренда
            if growth > 20:
                trend = "🚀 Взрывной рост"
            elif growth > 10:
                trend = "📈 Сильный рост"
            elif growth > 0:
                trend = "↗️ Рост"
            elif growth < -20:
                trend = "⚠️ Обвал"
            elif growth < -10:
                trend = "📉 Сильный спад"
            elif growth < 0:
                trend = "↘️ Спад"
            else:
                trend = "➡️ Стабильно"

            self.tree.insert("", "end", values=(
                period,
                count,
                cumulative,
                f"{growth:+.1f}%" if prev_count > 0 else "Н/Д",
                trend
            ))

            prev_count = count

        # Обновляем статистику
        avg_per_period = total_clients / len(data) if data else 0
        stats_text = f"""
        📊 СТАТИСТИКА: Всего клиентов: {total_clients:,} | Периодов: {len(data)} 
        Среднее за период: {avg_per_period:.1f} | Макс. рост: {max_growth:.1f}% ({max_growth_period})
        Минимальный рост: {min_growth:.1f}% ({min_growth_period})
        """
        self.stats_label.config(text=stats_text)

        return data

    def update_chart(self):
        """Обновление графика"""
        period = self.period_var.get()
        data = self.load_data(period)

        # Очищаем предыдущий график
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Создаем новый график
        if data:
            self.create_default_chart(data, period)

    def create_default_chart(self, data, period):
        """Создание стандартного графика"""
        periods = [row[0] for row in data]
        counts = [row[1] for row in data]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # График 1: Столбчатая диаграмма
        bars = ax1.bar(periods, counts, color='skyblue', alpha=0.7)
        ax1.set_title(f'Динамика регистрации клиентов ({period})', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Период')
        ax1.set_ylabel('Новых клиентов')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # Добавляем значения на столбцы
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                     f'{count}', ha='center', va='bottom', fontsize=9)

        # График 2: Линейный тренд
        cumulative = [row[2] for row in data]
        ax2.plot(periods, cumulative, 'g-', linewidth=2, marker='o', markersize=5)
        ax2.set_title('Накопительный итог', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Период')
        ax2.set_ylabel('Всего клиентов')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        # Встраиваем в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        return fig

    def show_bar_chart(self):
        """Показать только столбчатую диаграмму"""
        period = self.period_var.get()
        data = self.load_data(period)

        if not data:
            messagebox.showwarning("Нет данных", "Нет данных для построения графика")
            return

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Столбчатая диаграмма")
        chart_window.geometry("900x500")

        periods = [row[0] for row in data]
        counts = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF6B6B' if i % 3 == 0 else '#4ECDC4' if i % 3 == 1 else '#45B7D1' for i in range(len(periods))]

        bars = ax.bar(periods, counts, color=colors, edgecolor='black')

        ax.set_title(f'Регистрация клиентов по периодам ({period})', fontsize=16, fontweight='bold')
        ax.set_xlabel('Период', fontsize=12)
        ax.set_ylabel('Количество клиентов', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')

        # Поворачиваем подписи
        plt.xticks(rotation=45, ha='right')

        # Добавляем значения
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(chart_window, text="Закрыть",
                   command=chart_window.destroy).pack(pady=5)

    def show_line_chart(self):
        """Показать линейный график с трендом"""
        period = self.period_var.get()
        data = self.load_data(period)

        if not data:
            messagebox.showwarning("Нет данных", "Нет данных для построения графика")
            return

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Линейный график с трендом")
        chart_window.geometry("900x500")

        periods = [row[0] for row in data]
        counts = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(10, 6))

        # Линия тренда
        ax.plot(periods, counts, 'b-', linewidth=2, marker='o', markersize=8,
                label='Новые клиенты', markerfacecolor='red')

        # Скользящее среднее (тренд)
        window = 3
        moving_avg = []
        for i in range(len(counts)):
            if i < window - 1:
                moving_avg.append(None)
            else:
                avg = sum(counts[i - window + 1:i + 1]) / window
                moving_avg.append(avg)

        # Отображаем только валидные значения
        valid_periods = periods[window - 1:]
        valid_avg = moving_avg[window - 1:]
        ax.plot(valid_periods, valid_avg, 'r--', linewidth=3, label=f'Тренд (ср. {window} периода)')

        ax.set_title(f'Тренд регистрации клиентов ({period})', fontsize=16, fontweight='bold')
        ax.set_xlabel('Период', fontsize=12)
        ax.set_ylabel('Количество клиентов', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(chart_window, text="Закрыть",
                   command=chart_window.destroy).pack(pady=5)

    def compare_years(self):
        """Сравнение данных за разные годы"""
        query = """
        SELECT 
            strftime('%Y', registration_date) as year,
            strftime('%m', registration_date) as month,
            COUNT(*) as count
        FROM clients
        WHERE strftime('%Y', registration_date) IN ('2023', '2024', '2025')
        GROUP BY year, month
        ORDER BY year, month
        """

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        if not data:
            messagebox.showwarning("Нет данных", "Нет данных для сравнения")
            return

        # Группируем по годам
        years_data = {}
        for year, month, count in data:
            if year not in years_data:
                years_data[year] = {}
            years_data[year][int(month)] = count

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Сравнение по годам")
        chart_window.geometry("900x500")

        fig, ax = plt.subplots(figsize=(10, 6))

        months = list(range(1, 13))
        month_names = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                       'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD166']
        color_idx = 0

        for year in sorted(years_data.keys()):
            counts = [years_data[year].get(month, 0) for month in months]
            ax.plot(month_names, counts, marker='o', linewidth=2,
                    label=f'{year} год', color=colors[color_idx % len(colors)])
            color_idx += 1

        ax.set_title('Сравнение регистрации по месяцам за разные годы',
                     fontsize=16, fontweight='bold')
        ax.set_xlabel('Месяц', fontsize=12)
        ax.set_ylabel('Количество клиентов', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(chart_window, text="Закрыть",
                   command=chart_window.destroy).pack(pady=5)

    def export_data(self):
        """Экспорт данных в CSV файл"""
        period = self.period_var.get()
        data = self.load_data(period)

        if not data:
            messagebox.showwarning("Нет данных", "Нет данных для экспорта")
            return

        filename = f"trend_analysis_{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Период', 'Новых клиентов', 'Накопительный итог', 'Примечание'])

                for row in data:
                    writer.writerow(row)

            messagebox.showinfo("Экспорт успешен",
                                f"✅ Данные экспортированы в файл:\n{filename}\n"
                                f"Всего записей: {len(data)}")
        except Exception as e:
            messagebox.showerror("Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")

    def show_help(self):
        """Показать справку по использованию"""
        help_text = """
        🎯 КАК ПОЛЬЗОВАТЬСЯ АЛГОРИТМОМ 2:

        1. ПРИ ЗАПУСКЕ программа автоматически:
           • Создает базу данных 'trend_analysis.db'
           • Генерирует демо-данные за 2 года (24 месяца)
           • Показывает графики и таблицу

        2. ВЫБЕРИТЕ ПЕРИОД АНАЛИЗА:
           • Помесячно - детальная помесячная статистика
           • Поквартально - данные по кварталам
           • Погодно - годовые итоги

        3. КНОПКИ И ИХ ФУНКЦИИ:

           🔄 Обновить график - основной график в главном окне
           📊 Столбчатая диаграмма - откроется новое окно со столбчатой диаграммой
           📈 Линейный график - окно с линейным графиком и трендом
           📉 Сравнить годы - сравнение данных за разные годы
           📄 Экспорт данных - сохранить данные в CSV файл
           ℹ️ Справка - эта инструкция

        4. ЧТО ПОКАЗЫВАЕТСЯ:

           В ВЕРХНЕЙ ЧАСТИ:
           • Два графика: динамика и накопительный итог

           В ТАБЛИЦЕ:
           • Период (месяц/квартал/год)
           • Количество новых клиентов
           • Накопительный итог (общее количество)
           • Рост в % по сравнению с предыдущим периодом
           • Тренд (иконка и текст)

           ПОД ТАБЛИЦЕЙ:
           • Общая статистика

        5. 💡 СОВЕТЫ:
           • Используйте "Сравнить годы" для выявления сезонности
           • Экспортируйте данные для дальнейшего анализа в Excel
           • Красная линия на линейном графике показывает тренд (скользящее среднее)

        ⚠️ ВНИМАНИЕ: Все данные генерируются автоматически при первом запуске.
        """

        help_window = tk.Toplevel(self.root)
        help_window.title("Справка по использованию")
        help_window.geometry("700x600")

        text_widget = tk.Text(help_window, wrap="word", font=("Arial", 10))
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

        scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(help_window, text="Закрыть",
                   command=help_window.destroy).pack(pady=10)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationTrendApp(root)
    root.mainloop()