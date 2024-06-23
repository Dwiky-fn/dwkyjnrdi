import json
import streamlit as st
import pandas as pd
import time

def read_json(file_path):
    '''Menggunakan file JSON'''
    with open(file_path, 'r') as file:
        data = json.load(file)
    products = data['Sheet1']
    products.sort(key=lambda x: x['NAMA'])
    return products

def substring_search(products, target_name):
    '''Pencarian produk yang mengandung kata kunci'''
    return [product for product in products if target_name.lower() in product['NAMA'].lower()]

def binary_search(products, target_name):
    '''Binary search untuk produk dengan nama tepat'''
    low, high = 0, len(products) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_name = products[mid]['NAMA']
        if mid_name == target_name:
            return products[mid]
        elif mid_name < target_name:
            low = mid + 1
        else:
            high = mid - 1
    return None

def sequential_search(data, kolom, item):
    '''Sequential search untuk produk dengan nama tepat'''
    for pos in range(len(data)):
        if data[pos][kolom] == item:
            return True, pos
    return False, -1

def main():
    '''UI'''

    st.markdown( #membuat background
    """
    <style>
    .stApp {
        background-image: url('https://img.freepik.com/free-photo/wooden-board-empty-table-blurred-background-perspective-brown-wood-blur-department-store-can-be-used-display-montage-your-products-mock-up-display-product_1253-1458.jpg?w=996&t=st=1718850607~exp=1718851207~hmac=628c0e746574ae08a5d2540d14ac534aa5cee11604200d800ca32a6b5177dfd8');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    st.header('Pencarian Produk', divider='orange')

    file_path = 'produk.json'
    
    # Metode pencarian
    metode = st.radio("Pilih metode pencarian", ('Substring', 'Binary', 'Sequential'))
    
    # Kata kunci pencarian
    target_name = st.text_input("Masukkan nama produk").upper()

    if st.button('Cari'):
        products = read_json(file_path)
        
        if metode == 'Substring':
            start_time = time.time()
            # Pencarian substring
            filtered_products = substring_search(products, target_name)
            end_time = time.time()
            execution_time = end_time - start_time

            if filtered_products:
                st.write(f"Produk yang mengandung {target_name} ditemukan (substring search):")
                df = pd.DataFrame(filtered_products)
                for col in df.columns:
                    if df[col].dtype == 'float64' or df[col].dtype == 'int64':
                st.dataframe(df)
            else:
                st.write("Produk tidak ditemukan (substring search)")

        elif metode == 'Binary':
            start_time = time.time()
            # Pencarian binary
            found_product = binary_search(products, target_name)
            end_time = time.time()
            execution_time = end_time - start_time

            if found_product:
                st.write("Produk ditemukan (binary search):")
                df = pd.DataFrame([found_product])
                for col in df.columns:
                    if df[col].dtype == 'float64' or df[col].dtype == 'int64':
                st.dataframe(df)
            else:
                st.write("Produk tidak ditemukan (binary search)")

        elif metode == 'Sequential':
            start_time = time.time()
            # Pencarian sequential
            found, position = sequential_search(products, 'NAMA', target_name)
            end_time = time.time()
            execution_time = end_time - start_time

            if found:
                st.write("Produk ditemukan (sequential search):")
                df = pd.DataFrame([products[position]])
                for col in df.columns:
                    if df[col].dtype == 'float64' or df[col].dtype == 'int64':
                st.dataframe(df)
            else:
                st.write("Produk tidak ditemukan (sequential search)")
        
        # Display execution time
        st.write(f"Waktu eksekusi untuk metode {metode}: {execution_time:.6f} detik")

if __name__ == "__main__":
    main()
