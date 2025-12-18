import streamlit as st
import pandas as pd 

st.set_page_config(
    page_title="TRIPLE KICK SPORT - Toko Online",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon=":soccer:",
)

if 'page' not in st.session_state:
    st.session_state.page = "products"
if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'order_confirmed' not in st.session_state:
    st.session_state.order_confirmed = None 

PRODUCTS = {
    "sepatu futsal specs lightspeed reborn dazling blue": {
        "price": 499000, 
        "sizes": ["39", "40", "41", "42", "43"], 
        "image_url": "https://down-id.img.susercontent.com/file/id-11134207-7rbk6-mab2k1j2kfa8f6" 
    },
    "Sepatu sepak Bola ortuseight Raiden": {
        "price": 350000, 
        "sizes": ["39", "40", "41", "42", "43"], 
        "image_url": "https://down-id.img.susercontent.com/file/sg-11134201-23010-meepid8rczlv10" 
    },
    "sepatu sepak bola specs lightspeed 20": {
        "price": 399000, 
        "sizes": ["39", "40", "41", "42", "43"], 
        "image_url": "https://down-id.img.susercontent.com/file/id-11134207-7rasg-m3bv02k3bjkkbf" 
    },
    "sepatu futsal ortuseight catalyst liberte v2": {
        "price": 599000, 
        "sizes": ["39", "40", "41", "42", "43"], 
        "image_url": "https://down-id.img.susercontent.com/file/id-11134207-7quky-lesdsotszkav91" 
    },
    "sepatu futsal specs ls omega in": {
        "price": 450000,
        "sizes": ["39", "40", "41", "42", "43"],
        "image_url": "https://down-id.img.susercontent.com/file/id-11134207-7r98v-lpddap2ffs5p28"
    },
    "sepatu bola ortuseight catalyst wave fg": {
        "price": 550000,
        "sizes": ["39", "40", "41", "42", "43"],
        "image_url": "https://down-id.img.susercontent.com/file/id-11134207-7r991-lr6v5rb25abhfe"
    },
    "sepatu futsal specs swervo vortex in": {
        "price": 480000,
        "sizes": ["39", "40", "41", "42", "43"],
        "image_url": "https://img.lazcdn.com/g/p/52f2eac7c7c2ba1332df65d715b0e56b.jpg_720x720q80.jpg"
    },
    "sepatu bola ortuseight catalyst flash fg": {
        "price": 530000,
        "sizes": ["39", "40", "41", "42", "43"],
        "image_url": "https://assets-alpha.ass8c.upcloudobjects.com/0ri3yu6sr6afbqhrqgxwpq/images/19249-sg-11134201-7raty-ma3xyf0xm7fw1c.png"
    },
    "sepatu futsal specs swervo lightning in": {
        "price": 470000,
        "sizes": ["39", "40", "41", "42", "43"],
        "image_url": "https://img.lazcdn.com/g/p/fe7e2b34478b071de4de8ede4aec34a8.jpg_720x720q80.jpg"
    },
}

PAYMENT_DETAILS = {
    "Transfer Bank (BCA/Mandiri)": {
        "BCA": "1234 567 890 a.n. TRIPLE KICK",
        "Mandiri": "9876 543 210 a.n. TRIPLE KICK"
    },
    "E-Wallet (GoPay/OVO/Dana)": {
        "GoPay": "0812 3456 7890 a.n. TRIPLE KICK",
        "OVO": "0812 3456 7890 a.n. TRIPLE KICK",
        "Dana": "0812 3456 7890 a.n. TRPLE KICK"
    }
}


def delete_item(index):
    if 0 <= index < len(st.session_state.cart):
        st.session_state.cart.pop(index)
        st.rerun() 

def set_page(page_name):
    
    if page_name != "checkout":
        st.session_state.order_confirmed = None
        
    st.session_state.page = page_name



def display_products():
    st.header("⚽ Katalog Produk TRIPLE KICK SPORT")
    st.markdown("---")

    for product_name, data in PRODUCTS.items():
        price_formatted = f"Rp {data['price']:,}".replace(",", ".")
        
        col_img, col_info, col_form = st.columns([1.5, 3, 2])

        with col_img:
            st.image(data['image_url'], caption=product_name, width=150)

        with col_info:
            st.subheader(product_name)
            st.write(f"**Harga:** {price_formatted}")
            st.write(f"**Ukuran Tersedia:** {', '.join(data['sizes'])}")
        
        with col_form:
            selected_size = st.selectbox(
                "Pilih Ukuran", data['sizes'], key=f"size_{product_name}" 
            )
            quantity = st.number_input(
                "Jumlah", min_value=1, max_value=10, value=1, step=1, key=f"qty_{product_name}"
            )
            
            if st.button("🛒 Tambahkan ke Keranjang", key=f"add_{product_name}"):
                item = {
                    "name": product_name,
                    "size": selected_size,
                    "quantity": quantity,
                    "price": data['price'],
                    "subtotal": data['price'] * quantity
                }
                st.session_state.cart.append(item)
                st.success(f"{quantity}x **{product_name}** ({selected_size}) berhasil ditambahkan ke keranjang!")
        
        st.markdown("---")


def display_cart():
    if not st.session_state.cart:
        st.header("🛒 Keranjang Belanja Anda")
        st.info("Keranjang Anda masih kosong. Silakan pilih produk di halaman Katalog.")
        return

    st.header("🛒Rincian Keranjang Belanja")
    st.markdown("---")

    total_price = 0
    
   
    for i, item in enumerate(st.session_state.cart):
        col_item, col_delete = st.columns([4, 1])
        
        subtotal_formatted = f"Rp {item['subtotal']:,}".replace(",", ".")
        
        with col_item:
            st.markdown(f"**{item['name']}** ({item['size']}) x {item['quantity']}")
            st.caption(f"Subtotal: {subtotal_formatted}")
            
        with col_delete:
            st.button("❌ Hapus", 
                      key=f"delete_btn_{i}_{item['name']}",
                      on_click=delete_item,
                      args=(i,)) 
        
        total_price += item['subtotal']
        st.markdown("---")

    total_price_formatted = f"Rp {total_price:,}".replace(",", ".")
    st.markdown(f"## **Total Belanja: {total_price_formatted}**")
    
    if st.button("💰 Lanjutkan ke Pembayaran"):
        set_page("checkout")
        st.rerun()



def display_checkout():
    if not st.session_state.cart:
        set_page("products")
        st.warning("Keranjang Anda kosong. Dialihkan ke Katalog.")
        st.rerun()
        return
  
    if st.session_state.order_confirmed:
        details = st.session_state.order_confirmed
        
        st.title("🎉 Pesanan Berhasil Dibuat!")
        st.balloons()
        st.markdown("---")
        st.markdown(f"""
        ## **SELAMAT! Terima kasih telah berbelanja di TRIPLE KICK !**
        Pesanan Anda telah kami terima. Berikut adalah ringkasan dan instruksi pembayaran Anda:
        """)
        st.markdown("---")
        
        st.subheader("📦 Rincian Pesanan")
        item_rows = []
        for item in details['items']:
            item_rows.append({
                "Produk": item['name'],
                "Ukuran": item['size'],
                "Qty": item['quantity'],
                "Subtotal": f"Rp {item['subtotal']:,}".replace(",", ".")
            })
            
        df_items = pd.DataFrame(item_rows)
        st.dataframe(df_items, hide_index=True)
        st.markdown(f"### **Total Pembayaran: {details['total']}**")
        st.markdown("---")

        st.subheader("💳 Instruksi Pembayaran")
        
        payment_method = details['payment']
        if "Transfer Bank" in payment_method:
            st.info(f"Anda memilih **{payment_method}**. Mohon selesaikan pembayaran sebesar **{details['total']}** ke salah satu rekening berikut:")
            st.markdown("#### Detail Transfer Bank:")
            for bank, rek in PAYMENT_DETAILS["Transfer Bank (BCA/Mandiri)"].items():
                st.markdown(f"* **Bank {bank}:** `{rek}`")
            st.warning("Mohon segera konfirmasi pembayaran Anda setelah transfer berhasil.")
       
        elif "E-Wallet" in payment_method:
             st.info(f"Anda memilih **{payment_method}**. Mohon selesaikan pembayaran sebesar **{details['total']}** ke salah satu nomor E-Wallet berikut:")
             st.markdown("#### Detail E-Wallet:")
             for wallet, number in PAYMENT_DETAILS["E-Wallet (GoPay/OVO/Dana)"].items():
                 st.markdown(f"* **{wallet}:** `{number}`")
             st.warning("Pastikan nama pemilik E-Wallet sesuai dengan Nama Anda.")
        else: # COD
             st.info(f"""
             Anda memilih **{payment_method}**. 
             Pembayaran sebesar **{details['total']}** akan dilakukan secara tunai kepada kurir saat barang tiba.
             """)
        
        st.markdown("---")
        st.subheader("👤 Data Pengiriman")
        st.markdown(f"""
        * **Nama Penerima:** {details['name']}
        * **Alamat:** {details['address']}
        * **Nomor HP:** {details['phone']}
        * **Email:** {details['email']}
        """)

      
        def reset_state_after_order():
            st.session_state.cart = []
            st.session_state.order_confirmed = None
            set_page("products")
            
        if st.button("Kembali Berbelanja", on_click=reset_state_after_order):
            pass

   
    else:
        st.header("💰 3. Data Pengiriman & Pembayaran")
        st.markdown("---")
        
        total_price = sum(item['subtotal'] for item in st.session_state.cart)
        total_price_formatted = f"Rp {total_price:,}".replace(",", ".")
        
        st.markdown(f"**Total Pembayaran: {total_price_formatted}**")
        st.info("Mohon lengkapi data di bawah ini untuk mengkonfirmasi pesanan Anda.")

        with st.form("checkout_form"):
            st.subheader("📝 Data Pengiriman")
            name = st.text_input("Nama Lengkap", max_chars=50)
            address = st.text_area("Alamat Lengkap (termasuk Kota/Kode Pos)", max_chars=200)
            phone = st.text_input("Nomor Telepon/HP", max_chars=15)
            email = st.text_input("Email", help="Untuk konfirmasi pesanan", max_chars=50)
            
            st.markdown("### Metode Pembayaran")
            payment_options = list(PAYMENT_DETAILS.keys()) + ["Bayar di Tempat (COD) - Khusus Area Tertentu"]
            payment_method = st.radio("Pilih Metode", payment_options)
            
            submitted = st.form_submit_button("✅ Konfirmasi dan Bayar Sekarang")

        if submitted:
            if name and address and phone and email:
               
                st.session_state.order_confirmed = {
                    "name": name,
                    "address": address,
                    "phone": phone,
                    "email": email,
                    "payment": payment_method,
                    "total": total_price_formatted,
                    "items": st.session_state.cart[:] 
                }
                # Pindah ke tampilan konfirmasi (yang berada di bagian atas fungsi ini)
                st.rerun() 
            else:
                st.error("Mohon lengkapi semua data pengiriman.")


with st.sidebar:
    st.image("assets/logo.jpeg", width=200)
    st.markdown("## 🛒 Tahapan Belanja")
    st.button("1️⃣ Katalog Produk", on_click=set_page, args=("products",))
    cart_count = len(st.session_state.cart)
    st.button(f"2️⃣ Keranjang ({cart_count} Item)", on_click=set_page, args=("cart",))
    st.button("3️⃣ Pembayaran/Finalisasi", on_click=set_page, args=("checkout",))
    st.session_state.page == "checkout"


if st.session_state.page == "products":
    display_products()
elif st.session_state.page == "cart":
    display_cart()
elif st.session_state.page == "checkout":

    display_checkout()

