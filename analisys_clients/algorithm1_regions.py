# import sqlite3
# import tkinter as tk
# from tkinter import ttk, messagebox
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from datetime import datetime, timedelta
# import random
# import csv
#
#
# class RegionalDistributionApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Алгоритм 1: Анализ регионального распределения")
#         self.root.geometry("1000x700")
#
#         # Центрируем окно
#         self.center_window()
#
#         # Создаем демо-базу
#         self.create_demo_database()
#
#         # Подключаемся к базе
#         self.conn = sqlite3.connect("regional_analysis.db")
#         self.cursor = self.conn.cursor()
#
#         # Настройка стилей
#         self.setup_styles()
#
#         # Создаем интерфейс
#         self.create_widgets()
#
#         # Загружаем данные
#         self.load_data()
#
#     def center_window(self):
#         """Центрирование окна на экране"""
#         self.root.update_idletasks()
#         width = 1000
#         height = 700
#         x = (self.root.winfo_screenwidth() // 2) - (width // 2)
#         y = (self.root.winfo_screenheight() // 2) - (height // 2)
#         self.root.geometry(f'{width}x{height}+{x}+{y}')
#
#     def setup_styles(self):
#         """Настройка стилей для красивого интерфейса"""
#         style = ttk.Style()
#         style.theme_use('clam')
#         style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
#         style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
#         style.configure('Green.TButton', background='#4CAF50', foreground='white')
#         style.configure('Blue.TButton', background='#3498db', foreground='white')
#
#     def create_demo_database(self):
#         """Создание демонстрационной базы данных"""
#         conn = sqlite3.connect("regional_analysis.db")
#         cursor = conn.cursor()
#
#         # Создаем таблицу клиентов
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS clients (
#             id INTEGER PRIMARY KEY,
#             name TEXT,
#             region TEXT,
#             registration_date DATE,
#             total_purchases REAL
#         )
#         ''')
#
#         # Проверяем, есть ли данные
#         cursor.execute("SELECT COUNT(*) FROM clients")
#         if cursor.fetchone()[0] == 0:
#             # Добавляем демо-данные
#             regions = [
#                 ('Москва', 120),
#                 ('Санкт-Петербург', 85),
#                 ('Новосибирск', 45),
#                 ('Екатеринбург', 38),
#                 ('Казань', 32),
#                 ('Нижний Новгород', 28),
#                 ('Краснодар', 25),
#                 ('Сочи', 18),
#                 ('Владивосток', 15),
#                 ('Калининград', 12),
#                 ('Ростов-на-Дону', 20),
#                 ('Уфа', 16),
#                 ('Волгоград', 14),
#                 ('Пермь', 13),
#                 ('Омск', 11)
#             ]
#
#             client_id = 1
#             for region_name, count in regions:
#                 for i in range(count):
#                     name = f"Клиент_{client_id}"
#                     date = datetime.now() - timedelta(days=random.randint(0, 365))
#                     purchases = random.randint(1000, 50000)
#
#                     cursor.execute(
#                         "INSERT INTO clients (name, region, registration_date, total_purchases) VALUES (?, ?, ?, ?)",
#                         (name, region_name, date.date(), purchases)
#                     )
#                     client_id += 1
#
#             print(f"✅ Создано {client_id - 1} демо-клиентов в {len(regions)} регионах")
#
#         conn.commit()
#         conn.close()
#
#     def create_widgets(self):
#         """Создание элементов интерфейса"""
#         # Основной контейнер
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.pack(fill=tk.BOTH, expand=True)
#
#         # Заголовок
#         title_label = ttk.Label(
#             main_frame,
#             text="📊 АНАЛИЗ РАСПРЕДЕЛЕНИЯ КЛИЕНТОВ ПО РЕГИОНАМ",
#             style='Title.TLabel'
#         )
#         title_label.pack(pady=10)
#
#         # Фрейм управления
#         control_frame = ttk.Frame(main_frame)
#         control_frame.pack(fill=tk.X, pady=10)
#
#         # Кнопки управления
#         buttons = [
#             ("🔄 Обновить данные", self.load_data, "Blue.TButton"),
#             ("📊 Круговая диаграмма", self.show_pie_chart, "Blue.TButton"),
#             ("📈 Столбчатая диаграмма", self.show_bar_chart, "Blue.TButton"),
#             ("📄 Экспорт в CSV", self.export_to_csv, "Green.TButton"),
#             ("🧹 Очистить таблицу", self.clear_table, ""),
#             ("ℹ️ Помощь", self.show_help, "")
#         ]
#
#         for text, command, style in buttons:
#             if style:
#                 btn = ttk.Button(control_frame, text=text, command=command, style=style)
#             else:
#                 btn = ttk.Button(control_frame, text=text, command=command)
#             btn.pack(side=tk.LEFT, padx=5)
#
#         # Панель с результатами
#         results_frame = ttk.LabelFrame(main_frame, text="Результаты анализа", padding="10")
#         results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
#
#         # Создаем таблицу для отображения данных
#         self.create_table(results_frame)
#
#         # Панель статистики
#         stats_frame = ttk.Frame(main_frame)
#         stats_frame.pack(fill=tk.X, pady=10)
#
#         self.stats_label = ttk.Label(
#             stats_frame,
#             text="",
#             font=('Arial', 10, 'bold')
#         )
#         self.stats_label.pack()
#
#     def create_table(self, parent):
#         """Создание таблицы для отображения данных"""
#         # Создаем Treeview с полосой прокрутки
#         table_frame = ttk.Frame(parent)
#         table_frame.pack(fill=tk.BOTH, expand=True)
#
#         # Определяем столбцы
#         columns = ("№", "Регион", "Кол-во клиентов", "Доля (%)", "Сумма покупок", "Сегмент")
#
#         self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
#
#         # Настраиваем заголовки
#         col_widths = [50, 180, 120, 100, 150, 100]
#         for idx, col in enumerate(columns):
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=col_widths[idx], anchor="center")
#
#         # Добавляем полосу прокрутки
#         scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
#         self.tree.configure(yscrollcommand=scrollbar.set)
#
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#
#     def load_data(self):
#         """Загрузка и отображение данных"""
#         try:
#             # Выполняем SQL-запрос для анализа
#             query = """
#             SELECT
#                 region,
#                 COUNT(*) as client_count,
#                 SUM(total_purchases) as total_sales,
#                 ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clients), 2) as percentage
#             FROM clients
#             WHERE region IS NOT NULL AND region != ''
#             GROUP BY region
#             ORDER BY client_count DESC
#             """
#
#             self.cursor.execute(query)
#             results = self.cursor.fetchall()
#
#             if not results:
#                 messagebox.showinfo("Нет данных", "В базе данных нет клиентов для анализа")
#                 return
#
#             # Очищаем таблицу
#             self.clear_table()
#
#             # Заполняем таблицу
#             total_clients = sum(row[1] for row in results)
#             total_sales = sum(row[2] for row in results)
#
#             for idx, (region, count, sales, percentage) in enumerate(results, 1):
#                 # Определяем сегмент
#                 if percentage > 15:
#                     segment = "🔴 Высокий"
#                     segment_color = "red"
#                 elif percentage > 5:
#                     segment = "🟡 Средний"
#                     segment_color = "orange"
#                 else:
#                     segment = "🟢 Низкий"
#                     segment_color = "green"
#
#                 self.tree.insert("", "end", values=(
#                     idx,
#                     region,
#                     f"{count:,}".replace(",", " "),
#                     f"{percentage}%",
#                     f"{sales:,.0f} ₽".replace(",", " "),
#                     segment
#                 ))
#
#             # Обновляем статистику
#             avg_per_region = total_clients / len(results) if results else 0
#             avg_sales_per_region = total_sales / len(results) if results else 0
#
#             stats_text = f"""
#             📊 СТАТИСТИКА:
#             Всего клиентов: {total_clients:,} | Регионов: {len(results)}
#             Среднее клиентов на регион: {avg_per_region:.1f}
#             Общий объем продаж: {total_sales:,.0f} ₽ | Средние продажи на регион: {avg_sales_per_region:,.0f} ₽
#             """
#             self.stats_label.config(text=stats_text)
#
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{str(e)}")
#
#     def clear_table(self):
#         """Очистка таблицы"""
#         for item in self.tree.get_children():
#             self.tree.delete(item)
#
#     def show_pie_chart(self):
#         """Показ круговой диаграммы"""
#         try:
#             # Получаем данные для графика
#             query = """
#             SELECT region, COUNT(*) as count
#             FROM clients
#             WHERE region IS NOT NULL AND region != ''
#             GROUP BY region
#             ORDER BY count DESC
#             LIMIT 8
#             """
#
#             self.cursor.execute(query)
#             data = self.cursor.fetchall()
#
#             if not data:
#                 messagebox.showwarning("Нет данных", "Нет данных для построения графика")
#                 return
#
#             # Создаем новое окно для графика
#             chart_window = tk.Toplevel(self.root)
#             chart_window.title("Круговая диаграмма распределения по регионам")
#             chart_window.geometry("800x600")
#
#             # Создаем график
#             regions = [row[0] for row in data]
#             counts = [row[1] for row in data]
#
#             fig, ax = plt.subplots(figsize=(10, 8))
#
#             # Круговая диаграмма
#             colors = plt.cm.Set3(range(len(regions)))
#             wedges, texts, autotexts = ax.pie(
#                 counts,
#                 labels=regions,
#                 autopct='%1.1f%%',
#                 startangle=90,
#                 colors=colors,
#                 explode=[0.05] * len(regions)  # Немного отделяем куски
#             )
#
#             # Делаем проценты жирными
#             for autotext in autotexts:
#                 autotext.set_fontsize(10)
#                 autotext.set_fontweight('bold')
#
#             ax.set_title('ТОП-8 регионов по количеству клиентов', fontsize=16, fontweight='bold')
#             ax.axis('equal')  # Чтобы круг был кругом
#
#             plt.tight_layout()
#
#             # Встраиваем в Tkinter
#             canvas = FigureCanvasTkAgg(fig, master=chart_window)
#             canvas.draw()
#             canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#
#             # Кнопка закрытия
#             ttk.Button(chart_window, text="Закрыть",
#                        command=chart_window.destroy).pack(pady=10)
#
#             # Кнопка сохранения
#             ttk.Button(chart_window, text="💾 Сохранить как PNG",
#                        command=lambda: self.save_figure(fig, "pie_chart")).pack(pady=5)
#
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось построить график:\n{str(e)}")
#
#     def show_bar_chart(self):
#         """Показ столбчатой диаграммы"""
#         try:
#             # Получаем данные для графика
#             query = """
#             SELECT region, COUNT(*) as count, SUM(total_purchases) as sales
#             FROM clients
#             WHERE region IS NOT NULL AND region != ''
#             GROUP BY region
#             ORDER BY count DESC
#             LIMIT 10
#             """
#
#             self.cursor.execute(query)
#             data = self.cursor.fetchall()
#
#             if not data:
#                 messagebox.showwarning("Нет данных", "Нет данных для построения графика")
#                 return
#
#             # Создаем новое окно для графика
#             chart_window = tk.Toplevel(self.root)
#             chart_window.title("Столбчатая диаграмма по регионам")
#             chart_window.geometry("900x600")
#
#             # Создаем график
#             regions = [row[0] for row in data]
#             counts = [row[1] for row in data]
#             sales = [row[2] / 1000 for row in data]  # В тысячах рублей
#
#             fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
#
#             # График 1: Количество клиентов
#             bars1 = ax1.bar(regions, counts, color='skyblue', edgecolor='black', alpha=0.7)
#             ax1.set_title('Количество клиентов по регионам (ТОП-10)', fontsize=14, fontweight='bold')
#             ax1.set_xlabel('Регион')
#             ax1.set_ylabel('Количество клиентов')
#             ax1.grid(True, alpha=0.3, axis='y')
#             ax1.tick_params(axis='x', rotation=45)
#
#             # Добавляем значения на столбцы
#             for bar in bars1:
#                 height = bar.get_height()
#                 ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
#                          f'{int(height)}', ha='center', va='bottom', fontsize=9)
#
#             # График 2: Сумма покупок
#             bars2 = ax2.bar(regions, sales, color='lightgreen', edgecolor='black', alpha=0.7)
#             ax2.set_title('Сумма покупок по регионам (тыс. ₽)', fontsize=14, fontweight='bold')
#             ax2.set_xlabel('Регион')
#             ax2.set_ylabel('Сумма покупок (тыс. ₽)')
#             ax2.grid(True, alpha=0.3, axis='y')
#             ax2.tick_params(axis='x', rotation=45)
#
#             # Добавляем значения на столбцы
#             for bar in bars2:
#                 height = bar.get_height()
#                 ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
#                          f'{height:,.0f}', ha='center', va='bottom', fontsize=9)
#
#             plt.tight_layout()
#
#             # Встраиваем в Tkinter
#             canvas = FigureCanvasTkAgg(fig, master=chart_window)
#             canvas.draw()
#             canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#
#             # Кнопки
#             button_frame = ttk.Frame(chart_window)
#             button_frame.pack(pady=10)
#
#             ttk.Button(button_frame, text="Закрыть",
#                        command=chart_window.destroy).pack(side=tk.LEFT, padx=5)
#
#             ttk.Button(button_frame, text="💾 Сохранить график",
#                        command=lambda: self.save_figure(fig, "bar_chart")).pack(side=tk.LEFT, padx=5)
#
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось построить график:\n{str(e)}")
#
#     def save_figure(self, fig, filename_prefix):
#         """Сохранение графика в файл"""
#         try:
#             from datetime import datetime
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"{filename_prefix}_{timestamp}.png"
#
#             fig.savefig(filename, dpi=300, bbox_inches='tight')
#             messagebox.showinfo("Сохранено", f"График сохранен в файл:\n{filename}")
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось сохранить график:\n{str(e)}")
#
#     def export_to_csv(self):
#         """Экспорт данных в CSV"""
#         try:
#             # Получаем данные для экспорта
#             query = """
#             SELECT
#                 region,
#                 COUNT(*) as client_count,
#                 SUM(total_purchases) as total_sales,
#                 ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clients), 2) as percentage,
#                 ROUND(AVG(total_purchases), 2) as avg_purchase
#             FROM clients
#             WHERE region IS NOT NULL AND region != ''
#             GROUP BY region
#             ORDER BY client_count DESC
#             """
#
#             self.cursor.execute(query)
#             results = self.cursor.fetchall()
#
#             if not results:
#                 messagebox.showwarning("Нет данных", "Нет данных для экспорта")
#                 return
#
#             # Создаем имя файла с timestamp
#             from datetime import datetime
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"regional_analysis_{timestamp}.csv"
#
#             # Экспортируем в файл
#             with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
#                 writer = csv.writer(file, delimiter=';')
#
#                 # Записываем заголовки
#                 writer.writerow(['Регион', 'Количество клиентов', 'Сумма покупок (₽)', 'Доля (%)', 'Средний чек (₽)'])
#
#                 # Записываем данные
#                 for region, count, sales, percentage, avg_purchase in results:
#                     writer.writerow([region, count, sales, percentage, avg_purchase])
#
#             messagebox.showinfo("Экспорт завершен",
#                                 f"✅ Данные успешно экспортированы в файл:\n{filename}\n"
#                                 f"Всего регионов: {len(results)}\n"
#                                 f"Формат: CSV с разделителем ';' (открывается в Excel)")
#
#         except Exception as e:
#             messagebox.showerror("Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")
#
#     def show_help(self):
#         """Показать справку по использованию"""
#         help_text = """
#         🎯 КАК ПОЛЬЗОВАТЬСЯ АЛГОРИТМОМ 1:
#
#         1. ПРИ ЗАПУСКЕ программа автоматически:
#            • Создает базу данных 'regional_analysis.db'
#            • Генерирует демо-клиентов в 15 регионах России
#            • Загружает данные в таблицу
#
#         2. В ТАБЛИЦЕ вы видите:
#            • Список регионов (отсортировано по количеству клиентов)
#            • Количество клиентов в каждом регионе
#            • Доля региона в процентах от общего числа клиентов
#            • Сумма всех покупок клиентов региона
#            • Сегмент (цветная иконка и текст):
#              🔴 Высокий - более 15% клиентов
#              🟡 Средний - от 5% до 15%
#              🟢 Низкий - менее 5%
#
#         3. КНОПКИ И ИХ ФУНКЦИИ:
#
#            🔄 Обновить данные - перезагружает данные из базы
#            📊 Круговая диаграмма - показывает ТОП-8 регионов на круговой диаграмме
#            📈 Столбчатая диаграмма - показывает ТОП-10 регионов с двумя графиками:
#               • Количество клиентов
#               • Сумма покупок (в тыс. рублей)
#            📄 Экспорт в CSV - сохраняет аналитику в CSV файл (открывается в Excel)
#            🧹 Очистить таблицу - очищает таблицу (данные остаются в базе)
#            ℹ️ Помощь - показывает эту инструкцию
#
#         4. ВНИЗУ ОКНА отображается общая статистика:
#            • Общее количество клиентов
#            • Количество регионов
#            • Среднее количество клиентов на регион
#            • Общий объем продаж
#            • Средние продажи на регион
#
#         5. 💡 СОВЕТЫ:
#            • Нажмите на заголовок столбца для сортировки (в некоторых версиях Python)
#            • Экспортируйте данные для детального анализа в Excel
#            • Используйте оба типа графиков для лучшего понимания данных
#
#         6. ⚠️ ВНИМАНИЕ:
#            • Все данные генерируются автоматически при первом запуске
#            • Для реальных данных замените функцию create_demo_database
#            • CSV файлы сохраняются в текущей папке с timestamp в имени
#         """
#
#         help_window = tk.Toplevel(self.root)
#         help_window.title("Справка по использованию")
#         help_window.geometry("700x600")
#
#         text_widget = tk.Text(help_window, wrap="word", font=("Arial", 10))
#         text_widget.insert("1.0", help_text)
#         text_widget.config(state="disabled")
#
#         scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_widget.yview)
#         text_widget.configure(yscrollcommand=scrollbar.set)
#
#         text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#
#         ttk.Button(help_window, text="Закрыть",
#                    command=help_window.destroy).pack(pady=10)
#
#
# # Запуск приложения
# if __name__ == "__main__":
#     # Указываем бэкенд для matplotlib (решает большинство проблем с графиками)
#     import matplotlib
#
#     matplotlib.use('TkAgg')  # Используем Tkinter-совместимый бэкенд
#
#     root = tk.Tk()
#     app = RegionalDistributionApp(root)
#     root.mainloop()


import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import random
import csv
import os


class RegionalDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритм 1: Анализ регионального распределения")
        self.root.geometry("1000x700")

        # Центрируем окно
        self.center_window()

        # Создаем демо-базу
        self.create_demo_database()

        # Подключаемся к базе
        try:
            self.conn = sqlite3.connect("regional_analysis.db")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка подключения",
                                 f"Не удалось подключиться к БД:\n{str(e)}")
            self.conn = None
            self.cursor = None

        # Настройка стилей
        self.setup_styles()

        # Создаем интерфейс
        self.create_widgets()

        # Загружаем данные
        if self.conn and self.cursor:
            self.load_data()

    def center_window(self):
        """Центрирование окна на экране"""
        try:
            self.root.update_idletasks()
            width = 1000
            height = 700
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
        except tk.TclError as e:
            print(f"Ошибка центрирования окна: {e}")

    def setup_styles(self):
        """Настройка стилей для красивого интерфейса"""
        try:
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
            style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
            style.configure('Green.TButton', background='#4CAF50', foreground='white')
            style.configure('Blue.TButton', background='#3498db', foreground='white')
        except tk.TclError as e:
            print(f"Ошибка настройки стилей: {e}")

    def create_demo_database(self):
        """Создание демонстрационной базы данных"""
        conn = None
        try:
            conn = sqlite3.connect("regional_analysis.db")
            cursor = conn.cursor()

            # Создаем таблицу клиентов
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                region TEXT,
                registration_date DATE,
                total_purchases REAL
            )
            ''')

            # Проверяем, есть ли данные
            cursor.execute("SELECT COUNT(*) FROM clients")
            count = cursor.fetchone()[0]

            if count == 0:
                # Добавляем демо-данные
                regions = [
                    ('Москва', 120),
                    ('Санкт-Петербург', 85),
                    ('Новосибирск', 45),
                    ('Екатеринбург', 38),
                    ('Казань', 32),
                    ('Нижний Новгород', 28),
                    ('Краснодар', 25),
                    ('Сочи', 18),
                    ('Владивосток', 15),
                    ('Калининград', 12),
                    ('Ростов-на-Дону', 20),
                    ('Уфа', 16),
                    ('Волгоград', 14),
                    ('Пермь', 13),
                    ('Омск', 11)
                ]

                client_id = 1
                for region_name, region_count in regions:
                    for i in range(region_count):
                        try:
                            name = f"Клиент_{client_id}"
                            date = datetime.now() - timedelta(days=random.randint(0, 365))
                            purchases = random.randint(1000, 50000)

                            cursor.execute(
                                "INSERT INTO clients (name, region, registration_date, total_purchases) VALUES (?, ?, ?, ?)",
                                (name, region_name, date.date(), purchases)
                            )
                            client_id += 1
                        except Exception as e:
                            print(f"Ошибка вставки записи: {e}")
                            continue

                print(f"✅ Создано {client_id - 1} демо-клиентов в {len(regions)} регионах")

            conn.commit()

        except sqlite3.Error as e:
            print(f"Ошибка при создании БД: {e}")
            if conn:
                conn.rollback()
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
        finally:
            if conn:
                conn.close()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        try:
            # Основной контейнер
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Заголовок
            title_label = ttk.Label(
                main_frame,
                text="📊 АНАЛИЗ РАСПРЕДЕЛЕНИЯ КЛИЕНТОВ ПО РЕГИОНАМ",
                style='Title.TLabel'
            )
            title_label.pack(pady=10)

            # Фрейм управления
            control_frame = ttk.Frame(main_frame)
            control_frame.pack(fill=tk.X, pady=10)

            # Кнопки управления
            buttons = [
                ("🔄 Обновить данные", self.load_data, "Blue.TButton"),
                ("📊 Круговая диаграмма", self.show_pie_chart, "Blue.TButton"),
                ("📈 Столбчатая диаграмма", self.show_bar_chart, "Blue.TButton"),
                ("📄 Экспорт в CSV", self.export_to_csv, "Green.TButton"),
                ("🧹 Очистить таблицу", self.clear_table, ""),
                ("ℹ️ Помощь", self.show_help, "")
            ]

            for text, command, style in buttons:
                try:
                    if style:
                        btn = ttk.Button(control_frame, text=text, command=command, style=style)
                    else:
                        btn = ttk.Button(control_frame, text=text, command=command)
                    btn.pack(side=tk.LEFT, padx=5)
                except Exception as e:
                    print(f"Ошибка создания кнопки {text}: {e}")

            # Панель с результатами
            results_frame = ttk.LabelFrame(main_frame, text="Результаты анализа", padding="10")
            results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

            # Создаем таблицу для отображения данных
            self.create_table(results_frame)

            # Панель статистики
            stats_frame = ttk.Frame(main_frame)
            stats_frame.pack(fill=tk.X, pady=10)

            self.stats_label = ttk.Label(
                stats_frame,
                text="",
                font=('Arial', 10, 'bold')
            )
            self.stats_label.pack()

        except Exception as e:
            messagebox.showerror("Ошибка интерфейса",
                                 f"Не удалось создать элементы интерфейса:\n{str(e)}")

    def create_table(self, parent):
        """Создание таблицы для отображения данных"""
        try:
            # Создаем Treeview с полосой прокрутки
            table_frame = ttk.Frame(parent)
            table_frame.pack(fill=tk.BOTH, expand=True)

            # Определяем столбцы
            columns = ("№", "Регион", "Кол-во клиентов", "Доля (%)", "Сумма покупок", "Сегмент")

            self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

            # Настраиваем заголовки
            col_widths = [50, 180, 120, 100, 150, 100]
            for idx, col in enumerate(columns):
                self.tree.heading(col, text=col)
                self.tree.column(col, width=col_widths[idx], anchor="center")

            # Добавляем полосу прокрутки
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)

            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        except tk.TclError as e:
            messagebox.showerror("Ошибка таблицы",
                                 f"Не удалось создать таблицу:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось создать таблицу:\n{str(e)}")

    def load_data(self):
        """Загрузка и отображение данных с комплексной обработкой ошибок"""
        try:
            # ============ УРОВЕНЬ 1: ПРОВЕРКА ПОДКЛЮЧЕНИЯ К БД ============
            if not self.conn:
                raise sqlite3.Error("Отсутствует подключение к базе данных")

            if not self.cursor:
                raise sqlite3.Error("Не инициализирован курсор базы данных")

            # ============ УРОВЕНЬ 2: ВЫПОЛНЕНИЕ ЗАПРОСА ============
            query = """
            SELECT 
                region,
                COUNT(*) as client_count,
                SUM(total_purchases) as total_sales,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clients), 2) as percentage
            FROM clients
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region
            ORDER BY client_count DESC
            """

            # Проверка синтаксиса запроса
            if not query or len(query.strip()) == 0:
                raise ValueError("Пустой SQL-запрос")

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # ============ УРОВЕНЬ 3: ВАЛИДАЦИЯ РЕЗУЛЬТАТОВ ============
            if results is None:
                raise TypeError("Получен некорректный тип данных от БД")

            if len(results) == 0:
                # Информационное сообщение, не критическая ошибка
                messagebox.showinfo(
                    "Нет данных",
                    "В базе данных отсутствуют клиенты для анализа.\n"
                    "Будут использованы демонстрационные данные."
                )
                # Автоматическое восстановление - создаем демо-данные
                self.create_demo_database()
                # Повторный запрос
                self.cursor.execute(query)
                results = self.cursor.fetchall()

                if len(results) == 0:
                    raise RuntimeError("Не удалось создать демонстрационные данные")

            # ============ УРОВЕНЬ 4: ВАЛИДАЦИЯ СТРУКТУРЫ ДАННЫХ ============
            for row in results:
                # Проверка количества полей
                if len(row) != 4:
                    raise ValueError(f"Некорректная структура данных: ожидалось 4 поля, получено {len(row)}")

                # Проверка типов данных
                region, count, sales, percentage = row

                if not isinstance(region, str):
                    raise TypeError(f"Название региона должно быть строкой, получено {type(region)}")

                if not isinstance(count, int) or count < 0:
                    raise ValueError(f"Количество клиентов должно быть положительным целым числом, получено {count}")

                if not isinstance(sales, (int, float)) or sales < 0:
                    raise ValueError(f"Сумма покупок должна быть положительным числом, получено {sales}")

                if not isinstance(percentage, (int, float)) or percentage < 0 or percentage > 100:
                    raise ValueError(f"Процент должен быть в диапазоне 0-100, получено {percentage}")

            # ============ УРОВЕНЬ 5: ОЧИСТКА И ЗАПОЛНЕНИЕ ТАБЛИЦЫ ============
            self.clear_table()

            total_clients = 0
            total_sales = 0

            for idx, (region, count, sales, percentage) in enumerate(results, 1):
                # Валидация процентной доли для сегментации
                try:
                    if percentage > 15:
                        segment = "🔴 Высокий"
                    elif percentage > 5:
                        segment = "🟡 Средний"
                    else:
                        segment = "🟢 Низкий"
                except TypeError:
                    segment = "⚪ Не определен"

                # Безопасное форматирование чисел
                try:
                    formatted_count = f"{count:,}".replace(",", " ")
                    formatted_percentage = f"{percentage}%"
                    formatted_sales = f"{sales:,.0f} ₽".replace(",", " ")
                except (ValueError, TypeError) as e:
                    # Если форматирование не удалось, используем исходные значения
                    formatted_count = str(count)
                    formatted_percentage = f"{percentage}%"
                    formatted_sales = f"{sales} ₽"
                    print(f"Предупреждение: ошибка форматирования чисел - {e}")

                try:
                    self.tree.insert("", "end", values=(
                        idx,
                        region,
                        formatted_count,
                        formatted_percentage,
                        formatted_sales,
                        segment
                    ))
                except tk.TclError as e:
                    print(f"Ошибка вставки в таблицу: {e}")
                    continue

                total_clients += count
                total_sales += sales

            # ============ УРОВЕНЬ 6: РАСЧЕТ И ВАЛИДАЦИЯ СТАТИСТИКИ ============
            try:
                if len(results) > 0:
                    avg_per_region = total_clients / len(results)
                    avg_sales_per_region = total_sales / len(results)
                else:
                    avg_per_region = 0
                    avg_sales_per_region = 0

                # Проверка на бесконечность и NaN
                if not isinstance(avg_per_region, (int, float)) or avg_per_region == float('inf'):
                    avg_per_region = 0

                if not isinstance(avg_sales_per_region, (int, float)) or avg_sales_per_region == float('inf'):
                    avg_sales_per_region = 0

                stats_text = f"""
                📊 СТАТИСТИКА: 
                Всего клиентов: {total_clients:,} | Регионов: {len(results)} 
                Среднее клиентов на регион: {avg_per_region:.1f} 
                Общий объем продаж: {total_sales:,.0f} ₽ | Средние продажи на регион: {avg_sales_per_region:,.0f} ₽
                """
                self.stats_label.config(text=stats_text)

            except Exception as e:
                self.stats_label.config(text=f"📊 Ошибка расчета статистики: {str(e)}")

        except sqlite3.DatabaseError as e:
            messagebox.showerror(
                "Ошибка базы данных",
                f"Нарушение целостности БД:\n{str(e)}\n\n"
                "Попытка восстановления подключения..."
            )
            try:
                self.conn = sqlite3.connect("regional_analysis.db")
                self.cursor = self.conn.cursor()
                messagebox.showinfo("Восстановление", "Подключение к БД восстановлено")
            except Exception as recover_error:
                messagebox.showerror("Критическая ошибка",
                                     f"Не удалось восстановить подключение:\n{recover_error}")

        except sqlite3.OperationalError as e:
            messagebox.showerror(
                "Ошибка выполнения запроса",
                f"Не удалось выполнить SQL-запрос:\n{str(e)}\n\n"
                "Будет выполнена повторная инициализация БД."
            )
            self.create_demo_database()

        except ValueError as e:
            messagebox.showerror(
                "Ошибка данных",
                f"Обнаружены некорректные данные:\n{str(e)}"
            )
            try:
                with open("error_log.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"{datetime.now()}: ValueError - {str(e)}\n")
            except:
                pass

        except TypeError as e:
            messagebox.showerror(
                "Ошибка типов данных",
                f"Несоответствие типов данных:\n{str(e)}"
            )

        except MemoryError:
            messagebox.showerror(
                "Ошибка памяти",
                "Недостаточно памяти для обработки данных.\n"
                "Попробуйте уменьшить объем анализируемых данных."
            )

        except Exception as e:
            messagebox.showerror(
                "Непредвиденная ошибка",
                f"Произошла критическая ошибка:\n{str(e)}"
            )
            try:
                import traceback
                with open("critical_errors.log", "a", encoding="utf-8") as log_file:
                    log_file.write(f"{datetime.now()}: КРИТИЧЕСКАЯ ОШИБКА\n")
                    log_file.write(f"Тип: {type(e).__name__}\n")
                    log_file.write(f"Описание: {str(e)}\n")
                    log_file.write(f"Traceback: {traceback.format_exc()}\n")
                    log_file.write("-" * 80 + "\n")
            except:
                pass

    def clear_table(self):
        """Очистка таблицы"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
        except tk.TclError as e:
            print(f"Ошибка очистки таблицы: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка при очистке таблицы: {e}")

    def show_pie_chart(self):
        """Показ круговой диаграммы с полной обработкой ошибок визуализации"""

        # ============ ПРОВЕРКА 1: ДОСТУПНОСТЬ MATPLOTLIB ============
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ImportError as e:
            messagebox.showerror(
                "Ошибка библиотеки",
                f"Не удалось загрузить matplotlib:\n{str(e)}\n\n"
                "Установите библиотеку командой:\n"
                "pip install matplotlib"
            )
            return
        except Exception as e:
            messagebox.showerror(
                "Ошибка инициализации",
                f"Ошибка при настройке графического бэкенда:\n{str(e)}"
            )
            return

        # ============ ПРОВЕРКА 2: НАЛИЧИЕ ДАННЫХ ============
        try:
            if not self.cursor:
                raise ConnectionError("Отсутствует подключение к базе данных")

            query = """
            SELECT region, COUNT(*) as count 
            FROM clients 
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region 
            ORDER BY count DESC
            LIMIT 8
            """

            self.cursor.execute(query)
            data = self.cursor.fetchall()

        except sqlite3.Error as e:
            messagebox.showerror(
                "Ошибка БД",
                f"Не удалось получить данные для графика:\n{str(e)}"
            )
            return

        # ============ ПРОВЕРКА 3: ВАЛИДАЦИЯ ДАННЫХ ============
        if not data:
            messagebox.showwarning(
                "Нет данных",
                "В базе данных отсутствуют записи для построения графика.\n"
                "Создайте демо-данные или добавьте клиентов."
            )
            return

        for i, row in enumerate(data):
            if len(row) != 2:
                messagebox.showerror(
                    "Ошибка данных",
                    f"Некорректная структура данных в строке {i + 1}:\n"
                    f"Ожидалось 2 поля, получено {len(row)}"
                )
                return

            region, count = row

            if not region or not isinstance(region, str):
                messagebox.showerror(
                    "Ошибка данных",
                    f"Некорректное название региона в строке {i + 1}: {region}"
                )
                return

            if not isinstance(count, (int, float)) or count <= 0:
                messagebox.showerror(
                    "Ошибка данных",
                    f"Некорректное количество клиентов в регионе {region}: {count}"
                )
                return

        # ============ ПРОВЕРКА 4: СОЗДАНИЕ ГРАФИЧЕСКОГО ОКНА ============
        chart_window = None
        fig = None

        try:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Круговая диаграмма распределения по регионам")
            chart_window.geometry("800x600")

            # Центрирование окна графика
            chart_window.update_idletasks()
            width = 800
            height = 600
            x = (chart_window.winfo_screenwidth() // 2) - (width // 2)
            y = (chart_window.winfo_screenheight() // 2) - (height // 2)
            chart_window.geometry(f'{width}x{height}+{x}+{y}')

            def on_closing():
                try:
                    if fig:
                        plt.close(fig)
                except Exception as e:
                    print(f"Ошибка при закрытии фигуры: {e}")
                finally:
                    if chart_window:
                        chart_window.destroy()

            chart_window.protocol("WM_DELETE_WINDOW", on_closing)

        except tk.TclError as e:
            messagebox.showerror(
                "Ошибка интерфейса",
                f"Не удалось создать окно для графика:\n{str(e)}"
            )
            return

        # ============ ПРОВЕРКА 5: СОЗДАНИЕ ГРАФИКА ============
        try:
            # Подготовка данных
            regions = [row[0] for row in data]
            counts = [row[1] for row in data]

            # Защита от слишком длинных названий
            regions = [r[:20] + "..." if len(r) > 20 else r for r in regions]

            # Создание фигуры
            fig, ax = plt.subplots(figsize=(10, 8))

            # Проверка суммы значений
            if sum(counts) == 0:
                raise ValueError("Суммарное количество клиентов равно 0")

            # Генерация цветов
            try:
                colors = plt.cm.Set3(range(len(regions)))
            except Exception:
                colors = None

            # Построение диаграммы
            pie_kwargs = {
                'x': counts,
                'labels': regions,
                'autopct': '%1.1f%%',
                'startangle': 90,
                'explode': [0.05] * len(regions)
            }

            if colors is not None:
                pie_kwargs['colors'] = colors

            wedges, texts, autotexts = ax.pie(**pie_kwargs)

            # Настройка текста
            for autotext in autotexts:
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')

            ax.set_title(
                'ТОП-8 регионов по количеству клиентов',
                fontsize=16,
                fontweight='bold',
                pad=20
            )
            ax.axis('equal')
            plt.tight_layout()

        except ValueError as e:
            messagebox.showerror(
                "Ошибка построения",
                f"Некорректные данные для построения графика:\n{str(e)}"
            )
            if chart_window:
                chart_window.destroy()
            return

        except Exception as e:
            messagebox.showerror(
                "Ошибка визуализации",
                f"Не удалось построить круговую диаграмму:\n{str(e)}"
            )
            if chart_window:
                chart_window.destroy()
            return

        # ============ ПРОВЕРКА 6: ВСТРАИВАНИЕ В TKINTER ============
        try:
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        except Exception as e:
            messagebox.showerror(
                "Ошибка интеграции",
                f"Не удалось встроить график в интерфейс:\n{str(e)}"
            )
            plt.close(fig)
            if chart_window:
                chart_window.destroy()
            return

        # ============ ПРОВЕРКА 7: СОЗДАНИЕ КНОПОК УПРАВЛЕНИЯ ============
        try:
            button_frame = ttk.Frame(chart_window)
            button_frame.pack(pady=10)

            close_btn = ttk.Button(
                button_frame,
                text="Закрыть",
                command=on_closing
            )
            close_btn.pack(side=tk.LEFT, padx=5)

            save_btn = ttk.Button(
                button_frame,
                text="💾 Сохранить как PNG",
                command=lambda: self.save_figure_safe(fig, "pie_chart", chart_window)
            )
            save_btn.pack(side=tk.LEFT, padx=5)

        except Exception as e:
            print(f"Предупреждение: не удалось создать кнопки управления - {e}")

    def show_bar_chart(self):
        """Показ столбчатой диаграммы с полной обработкой ошибок"""

        # Проверка доступности matplotlib
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ImportError as e:
            messagebox.showerror(
                "Ошибка библиотеки",
                f"Не удалось загрузить matplotlib:\n{str(e)}"
            )
            return

        # Получение данных
        try:
            if not self.cursor:
                raise ConnectionError("Отсутствует подключение к базе данных")

            query = """
            SELECT region, COUNT(*) as count, SUM(total_purchases) as sales
            FROM clients 
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region 
            ORDER BY count DESC
            LIMIT 10
            """

            self.cursor.execute(query)
            data = self.cursor.fetchall()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные:\n{str(e)}")
            return

        # Валидация данных
        if not data:
            messagebox.showwarning("Нет данных", "Нет данных для построения графика")
            return

        # Создание окна
        chart_window = None
        fig = None

        try:
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Столбчатая диаграмма по регионам")
            chart_window.geometry("900x600")

            # Центрирование
            chart_window.update_idletasks()
            x = (chart_window.winfo_screenwidth() // 2) - (900 // 2)
            y = (chart_window.winfo_screenheight() // 2) - (600 // 2)
            chart_window.geometry(f'900x600+{x}+{y}')

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать окно:\n{str(e)}")
            return

        # Построение графика
        try:
            regions = [row[0] for row in data]
            counts = [row[1] for row in data]
            sales = [row[2] / 1000 for row in data]

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

            # График 1: Количество клиентов
            bars1 = ax1.bar(regions, counts, color='skyblue', edgecolor='black', alpha=0.7)
            ax1.set_title('Количество клиентов по регионам (ТОП-10)', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Количество клиентов')
            ax1.grid(True, alpha=0.3, axis='y')
            ax1.tick_params(axis='x', rotation=45)

            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                         f'{int(height)}', ha='center', va='bottom', fontsize=9)

            # График 2: Сумма покупок
            bars2 = ax2.bar(regions, sales, color='lightgreen', edgecolor='black', alpha=0.7)
            ax2.set_title('Сумма покупок по регионам (тыс. ₽)', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Регион')
            ax2.set_ylabel('Сумма покупок (тыс. ₽)')
            ax2.grid(True, alpha=0.3, axis='y')
            ax2.tick_params(axis='x', rotation=45)

            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                         f'{height:,.0f}', ha='center', va='bottom', fontsize=9)

            plt.tight_layout()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{str(e)}")
            if chart_window:
                chart_window.destroy()
            return

        # Встраивание графика
        try:
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            button_frame = ttk.Frame(chart_window)
            button_frame.pack(pady=10)

            ttk.Button(button_frame, text="Закрыть",
                       command=lambda: self.close_chart_window(chart_window, fig)).pack(side=tk.LEFT, padx=5)

            ttk.Button(button_frame, text="💾 Сохранить график",
                       command=lambda: self.save_figure_safe(fig, "bar_chart", chart_window)).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отобразить график:\n{str(e)}")
            plt.close(fig)
            if chart_window:
                chart_window.destroy()

    def close_chart_window(self, window, figure):
        """Безопасное закрытие окна с графиком"""
        try:
            if figure:
                plt.close(figure)
        except Exception as e:
            print(f"Ошибка при закрытии фигуры: {e}")
        finally:
            try:
                if window:
                    window.destroy()
            except Exception as e:
                print(f"Ошибка при закрытии окна: {e}")

    def save_figure_safe(self, fig, filename_prefix, parent_window=None):
        """Безопасное сохранение графика с обработкой всех возможных ошибок"""

        try:
            # ============ ПРОВЕРКА 1: ВАЛИДАЦИЯ ВХОДНЫХ ДАННЫХ ============
            if fig is None:
                raise ValueError("Объект фигуры графика отсутствует")

            if not filename_prefix or not isinstance(filename_prefix, str):
                filename_prefix = "chart"

            # ============ ПРОВЕРКА 2: ДОСТУПНОСТЬ ФАЙЛОВОЙ СИСТЕМЫ ============
            # Проверка прав на запись
            test_file = "_write_test.tmp"
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
            except PermissionError:
                messagebox.showerror(
                    "Ошибка доступа",
                    "Нет прав на запись в текущую папку.\n"
                    "Попробуйте запустить программу от имени администратора."
                )
                return
            except Exception as e:
                messagebox.showerror(
                    "Ошибка файловой системы",
                    f"Не удается создать файл в текущей папке:\n{str(e)}"
                )
                return

            # ============ ПРОВЕРКА 3: ГЕНЕРАЦИЯ ИМЕНИ ФАЙЛА ============
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{filename_prefix}_{timestamp}.png"
            except Exception:
                import random
                filename = f"{filename_prefix}_{random.randint(1000, 9999)}.png"

            # ============ ПРОВЕРКА 4: ПРОВЕРКА СУЩЕСТВОВАНИЯ ФАЙЛА ============
            if os.path.exists(filename):
                if not messagebox.askyesno(
                        "Файл существует",
                        f"Файл {filename} уже существует.\nПерезаписать его?"
                ):
                    name, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(f"{name}_{counter}{ext}"):
                        counter += 1
                        if counter > 1000:
                            raise RuntimeError("Не удалось сгенерировать уникальное имя")
                    filename = f"{name}_{counter}{ext}"

            # ============ ПРОВЕРКА 5: СОХРАНЕНИЕ ГРАФИКА ============
            try:
                fig.savefig(filename, dpi=300, bbox_inches='tight')
            except ValueError:
                # Повторная попытка с базовыми параметрами
                fig.savefig(filename)
            except PermissionError:
                messagebox.showerror("Ошибка доступа", f"Нет прав на запись файла {filename}")
                return
            except OSError as e:
                messagebox.showerror("Ошибка ввода-вывода", f"Ошибка при записи файла:\n{str(e)}")
                return

            # ============ ПРОВЕРКА 6: ВЕРИФИКАЦИЯ СОЗДАННОГО ФАЙЛА ============
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                if file_size == 0:
                    raise RuntimeError("Создан пустой файл")

                messagebox.showinfo(
                    "Сохранено",
                    f"✅ График сохранен в файл:\n{filename}\n"
                    f"Размер: {file_size} байт\n"
                    f"Разрешение: 300 DPI"
                )
            else:
                raise FileNotFoundError(f"Файл {filename} не найден")

        except Exception as e:
            messagebox.showerror(
                "Ошибка сохранения",
                f"Не удалось сохранить график:\n{str(e)}"
            )
            try:
                with open("save_errors.log", "a", encoding="utf-8") as log:
                    log.write(f"{datetime.now()}: Ошибка сохранения {filename_prefix}\n")
                    log.write(f"Ошибка: {str(e)}\n")
                    log.write("-" * 50 + "\n")
            except:
                pass

    def export_to_csv(self):
        """Экспорт данных в CSV с транзакционной моделью и полной валидацией"""

        # ============ ЭТАП 1: ПОДГОТОВКА И ВАЛИДАЦИЯ ДАННЫХ ============
        try:
            if not self.conn or not self.cursor:
                raise ConnectionError("Подключение к базе данных не установлено")

            # Проверка наличия таблицы
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
            if not self.cursor.fetchone():
                raise RuntimeError("Таблица 'clients' не существует")

            # Выполнение запроса
            query = """
            SELECT 
                region,
                COUNT(*) as client_count,
                SUM(total_purchases) as total_sales,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clients), 2) as percentage,
                ROUND(AVG(total_purchases), 2) as avg_purchase
            FROM clients
            WHERE region IS NOT NULL AND region != ''
            GROUP BY region
            ORDER BY client_count DESC
            """

            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Валидация результатов
            if not results:
                messagebox.showwarning("Нет данных", "В базе данных отсутствуют записи для экспорта")
                return

            # Валидация структуры
            for i, row in enumerate(results):
                if len(row) != 5:
                    raise ValueError(f"Некорректная структура данных в строке {i + 1}")

                if row[0] is None or str(row[0]).strip() == '':
                    raise ValueError(f"Обнаружен регион с пустым названием")

            self._export_data = results
            self._export_row_count = len(results)

        except Exception as e:
            messagebox.showerror("Ошибка подготовки данных", f"Не удалось подготовить данные:\n{str(e)}")
            return

        # ============ ЭТАП 2: ПРОВЕРКА ФАЙЛОВОЙ СИСТЕМЫ ============
        try:
            # Генерация имени файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"regional_analysis_{timestamp}"

            # Удаление недопустимых символов
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                if char in base_filename:
                    base_filename = base_filename.replace(char, '_')

            filename = f"{base_filename}.csv"

            # Проверка существования файла
            counter = 1
            while os.path.exists(filename):
                filename = f"{base_filename}_{counter}.csv"
                counter += 1
                if counter > 1000:
                    raise RuntimeError("Не удалось сгенерировать уникальное имя файла")

        except Exception as e:
            messagebox.showerror("Ошибка файловой системы", f"Не удалось подготовить файл:\n{str(e)}")
            return

        # ============ ЭТАП 3: ЗАПИСЬ ФАЙЛА ============
        temp_filename = filename + ".tmp"

        try:
            # Запись во временный файл
            with open(temp_filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')

                # Запись заголовков
                writer.writerow([
                    'Регион',
                    'Количество клиентов',
                    'Сумма покупок (₽)',
                    'Доля (%)',
                    'Средний чек (₽)'
                ])

                # Запись данных
                for row in results:
                    writer.writerow(row)

            # Переименование временного файла
            if os.path.exists(temp_filename):
                if os.path.exists(filename):
                    os.remove(filename)
                os.rename(temp_filename, filename)

            # Проверка созданного файла
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                messagebox.showinfo(
                    "Экспорт завершен",
                    f"✅ Данные экспортированы в файл:\n{filename}\n"
                    f"Регионов: {len(results)}\n"
                    f"Размер файла: {file_size} байт"
                )
            else:
                raise FileNotFoundError("Файл не был создан")

        except PermissionError:
            messagebox.showerror("Ошибка доступа", f"Нет прав на запись файла {filename}")
        except csv.Error as e:
            messagebox.showerror("Ошибка CSV", f"Ошибка при записи CSV:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")
        finally:
            # Очистка временного файла
            try:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
            except:
                pass

    def show_help(self):
        """Показать справку по использованию"""
        try:
            help_text = """
            🎯 КАК ПОЛЬЗОВАТЬСЯ АЛГОРИТМОМ 1:

            1. ПРИ ЗАПУСКЕ программа автоматически:
               • Создает базу данных 'regional_analysis.db'
               • Генерирует демо-клиентов в 15 регионах России
               • Загружает данные в таблицу

            2. В ТАБЛИЦЕ вы видите:
               • Список регионов (отсортировано по количеству клиентов)
               • Количество клиентов в каждом регионе
               • Доля региона в процентах от общего числа клиентов
               • Сумма всех покупок клиентов региона
               • Сегмент (цветная иконка и текст):
                 🔴 Высокий - более 15% клиентов
                 🟡 Средний - от 5% до 15%
                 🟢 Низкий - менее 5%

            3. КНОПКИ И ИХ ФУНКЦИИ:

               🔄 Обновить данные - перезагружает данные из базы
               📊 Круговая диаграмма - показывает ТОП-8 регионов на круговой диаграмме
               📈 Столбчатая диаграмма - показывает ТОП-10 регионов с двумя графиками
               📄 Экспорт в CSV - сохраняет аналитику в CSV файл
               🧹 Очистить таблицу - очищает таблицу (данные остаются в базе)
               ℹ️ Помощь - показывает эту инструкцию

            4. ВНИЗУ ОКНА отображается общая статистика

            5. ⚠️ ВНИМАНИЕ:
               • Все данные генерируются автоматически при первом запуске
               • CSV файлы сохраняются в текущей папке
            """

            help_window = tk.Toplevel(self.root)
            help_window.title("Справка по использованию")
            help_window.geometry("700x600")

            # Центрирование окна справки
            help_window.update_idletasks()
            x = (help_window.winfo_screenwidth() // 2) - (700 // 2)
            y = (help_window.winfo_screenheight() // 2) - (600 // 2)
            help_window.geometry(f'700x600+{x}+{y}')

            text_widget = tk.Text(help_window, wrap="word", font=("Arial", 10))
            text_widget.insert("1.0", help_text)
            text_widget.config(state="disabled")

            scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)

            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            ttk.Button(help_window, text="Закрыть",
                       command=help_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть справку:\n{str(e)}")

    def __del__(self):
        """Деструктор для корректного закрытия соединения с БД"""
        try:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Ошибка при закрытии соединения с БД: {e}")


# Запуск приложения
if __name__ == "__main__":
    try:
        # Указываем бэкенд для matplotlib
        import matplotlib

        matplotlib.use('TkAgg')

        root = tk.Tk()
        app = RegionalDistributionApp(root)
        root.mainloop()

    except KeyboardInterrupt:
        print("Программа прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}")
        import traceback

        traceback.print_exc()