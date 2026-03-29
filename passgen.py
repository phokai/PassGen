#!/usr/bin/env python3
"""
PassGen v2 - Parola Oluşturucu
Tek dosya halinde parola oluşturucu (tkinter arayüzü ile)
"""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass

# Core functionality
AMBIGUOUS = "0O1lI"


@dataclass
class Charset:
    upper: str = string.ascii_uppercase
    lower: str = string.ascii_lowercase
    digits: str = string.digits
    symbols: str = "!@#$%^&*()-_=+[]{}|;:,.<>?"


def build_pool(
    *,
    use_upper: bool,
    use_lower: bool,
    use_digits: bool,
    use_symbols: bool,
    exclude_ambiguous: bool,
) -> str:
    parts: list[str] = []
    if use_upper:
        parts.append(Charset.upper)
    if use_lower:
        parts.append(Charset.lower)
    if use_digits:
        parts.append(Charset.digits)
    if use_symbols:
        parts.append(Charset.symbols)
    pool = "".join(parts)
    if exclude_ambiguous:
        pool = "".join(c for c in pool if c not in AMBIGUOUS)
    return pool


def generate_password(
    length: int,
    *,
    use_upper: bool,
    use_lower: bool,
    use_digits: bool,
    use_symbols: bool,
    exclude_ambiguous: bool,
    ensure_each_selected: bool,
) -> str:
    pool = build_pool(
        use_upper=use_upper,
        use_lower=use_lower,
        use_digits=use_digits,
        use_symbols=use_symbols,
        exclude_ambiguous=exclude_ambiguous,
    )
    if not pool:
        raise ValueError("En az bir karakter kümesi seçmelisiniz.")
    if length < 1:
        raise ValueError("Uzunluk en az 1 olmalı.")

    required: list[str] = []
    if ensure_each_selected:
        if use_upper:
            u = Charset.upper
            if exclude_ambiguous:
                u = "".join(c for c in u if c not in AMBIGUOUS)
            if u:
                required.append(secrets.choice(u))
        if use_lower:
            lo = Charset.lower
            if exclude_ambiguous:
                lo = "".join(c for c in lo if c not in AMBIGUOUS)
            if lo:
                required.append(secrets.choice(lo))
        if use_digits:
            d = Charset.digits
            if exclude_ambiguous:
                d = "".join(c for c in d if c not in AMBIGUOUS)
            if d:
                required.append(secrets.choice(d))
        if use_symbols:
            required.append(secrets.choice(Charset.symbols))

    if len(required) > length:
        raise ValueError("Seçilen uzunluk, zorunlu karakterleri sığdırmıyor; uzunluğu artırın.")

    remaining = length - len(required)
    chars = required + [secrets.choice(pool) for _ in range(remaining)]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def password_entropy_bits(password: str, pool_size: int) -> float:
    import math
    if pool_size < 2 or not password:
        return 0.0
    return len(password) * math.log2(pool_size)


def strength_label(bits: float) -> str:
    if bits < 36:
        return "Zayıf"
    if bits < 60:
        return "Orta"
    if bits < 100:
        return "Güçlü"
    return "Çok güçlü"


# Tkinter Interface
import tkinter as tk
from tkinter import messagebox, ttk


class PasswordGeneratorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PassGen")
        self.geometry("450x500")
        self.minsize(400, 450)
        self.resizable(False, False)

        self.length_var = tk.IntVar(value=20)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=True)
        self.ensure_each_var = tk.BooleanVar(value=True)
        self.result_var = tk.StringVar(value="")
        self.strength_var = tk.StringVar(value="")

        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self._build_ui()
        self._generate()

    def _build_ui(self) -> None:
        main = ttk.Frame(self, padding=15)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=1)

        # Ana başlık
        ttk.Label(main, text="Parola Oluşturucu", font=("Helvetica", 16, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 15))

        # Seçenekler çerçevesi
        opts = ttk.LabelFrame(main, text="Seçenekler", padding=10)
        opts.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        opts.columnconfigure(1, weight=1)

        # Uzunluk satırı
        ttk.Label(opts, text="Uzunluk:").grid(row=0, column=0, sticky="w", pady=2)
        
        # Spinbox ve scrollbar
        spinbox_frame = ttk.Frame(opts)
        spinbox_frame.grid(row=0, column=1, sticky="ew", pady=2)
        spinbox_frame.columnconfigure(0, weight=1)
        
        self.length_spinbox = ttk.Spinbox(spinbox_frame, from_=4, to=64, textvariable=self.length_var, width=15)
        self.length_spinbox.grid(row=0, column=0, sticky="w")
        
        # Kaydırma çubuğu - Scale widget kullanarak daha stabil yapalım
        self.length_scale = ttk.Scale(spinbox_frame, from_=4, to=64, orient="horizontal", 
                                     command=self._on_scale_change)
        self.length_scale.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        self.length_scale.set(20)  # Başlangıç değeri
        
        # Scale ile spinbox senkronizasyonu
        self._trace_id = self.length_var.trace_add('write', self._on_var_change)

        # Checkbutton'lar
        ttk.Checkbutton(opts, text="Büyük harf (A-Z)", variable=self.upper_var, command=self._generate).grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(opts, text="Küçük harf (a-z)", variable=self.lower_var, command=self._generate).grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(opts, text="Rakamlar (0-9)", variable=self.digits_var, command=self._generate).grid(row=3, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(opts, text="Semboller (!@#...)", variable=self.symbols_var, command=self._generate).grid(row=4, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(opts, text="Belirsiz karakterleri çıkar (0, O, 1, l, I...)", variable=self.exclude_ambiguous_var, command=self._generate).grid(row=5, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(opts, text="Her seçili kümeden en az bir karakter", variable=self.ensure_each_var, command=self._generate).grid(row=6, column=0, columnspan=2, sticky="w", pady=2)

        # Sonuç çerçevesi
        res_frame = ttk.LabelFrame(main, text="Sonuç", padding=10)
        res_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        res_frame.columnconfigure(0, weight=1)

        self.result_entry = ttk.Entry(res_frame, textvariable=self.result_var, font=("Courier", 11), state="readonly", justify="center")
        self.result_entry.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Güç göstergesi
        self.strength_label = ttk.Label(res_frame, textvariable=self.strength_var, font=("Helvetica", 10))
        self.strength_label.grid(row=1, column=0, sticky="w")

        # Butonlar
        button_frame = ttk.Frame(main)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        button_frame.columnconfigure((0, 1, 2), weight=1)

        ttk.Button(button_frame, text="Yeni parola", command=self._generate).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Panoya kopyala", command=self._copy_to_clipboard).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Çıkış", command=self.quit).grid(row=0, column=2, padx=(5, 0))
        
        # Versiyon bilgisi - pencerenin en altına
        version_label = ttk.Label(self, text="PassGen v2.0", font=("Helvetica", 8), foreground="gray")
        version_label.place(relx=0.5, rely=0.98, anchor="s")
        
        # Başlangıçta scale'i doğru konuma getir
        self.after(100, lambda: self.length_scale.set(self.length_var.get()))

    def _on_scale_change(self, value) -> None:
        """Scale değiştiğinde spinbox değerini günceller (parola oluşturmaz)"""
        try:
            new_val = int(float(value))
            # trace'i geçici olarak kaldırıp tekrar ekleyerek sonsuz döngüyü önle
            self.length_var.trace_remove('write', self._trace_id)
            self.length_var.set(new_val)
            self._trace_id = self.length_var.trace_add('write', self._on_var_change)
        except:
            pass

    def _on_var_change(self, *args) -> None:
        """Variable değiştiğinde scale'i günceller ve parola oluşturur"""
        try:
            current_val = self.length_var.get()
            # Scale'i güncelle ama parola oluşturma (scale'den gelen değişiklik için)
            if not hasattr(self, '_updating_from_scale'):
                self._updating_from_scale = False
            if not self._updating_from_scale:
                self._updating_from_scale = True
                self.length_scale.set(current_val)
                self._generate()
                self._updating_from_scale = False
        except:
            pass

    def _generate(self, *args) -> None:
        try:
            pwd = generate_password(
                self.length_var.get(),
                use_upper=self.upper_var.get(),
                use_lower=self.lower_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
                exclude_ambiguous=self.exclude_ambiguous_var.get(),
                ensure_each_selected=self.ensure_each_var.get(),
            )
            self.result_var.set(pwd)
            pool = build_pool(
                use_upper=self.upper_var.get(),
                use_lower=self.lower_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
                exclude_ambiguous=self.exclude_ambiguous_var.get(),
            )
            bits = password_entropy_bits(pwd, len(pool))
            self.strength_var.set(f"Tahmini güç: {strength_label(bits)} (~{bits:.0f} bit)")
        except ValueError as exc:
            self.result_var.set("")
            self.strength_var.set(f"Hata: {exc}")

    def _copy_to_clipboard(self) -> None:
        pwd = self.result_var.get()
        if pwd:
            self.clipboard_clear()
            self.clipboard_append(pwd)
            self.update()
            messagebox.showinfo("Kopyalandı", "Parola panoya kopyalandı!")


# Main entry point
def main() -> None:
    app = PasswordGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
