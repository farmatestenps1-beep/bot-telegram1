import telebot
from telebot import types

TOKEN = '9202776983:AAFWVbMzPUXOirHJqgR8MXzX-TNwENspjnE'
ADMIN_ID = 6595022688

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def enviar_menu(message):
    user_id = message.from_user.id
    nome = message.from_user.first_name
    
    saldo = "R$ 0,00"
    nivel = "Classic"
    
    texto = (
        f"👤 **Nome:** {nome}\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"⭐ **Nível:** {nivel}\n"
        f"💰 **Saldo Disponível:** {saldo}\n\n"
        f"Escolha uma opção no menu abaixo:"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn_compra = types.InlineKeyboardButton("🛒 Compra Aleatória", callback_data="compra_aleatoria")
    btn_recarga = types.InlineKeyboardButton("💳 Recarregar", callback_data="recarga")
    btn_trocas = types.InlineKeyboardButton("🔄 Trocas & Testador", callback_data="trocas")
    btn_bin = types.InlineKeyboardButton("🔍 Consultar Bin", callback_data="consultar_bin")
    btn_nivel = types.InlineKeyboardButton("⭐ Consultar Nível", callback_data="consultar_nivel")
    
    # Adicionando botões em pares (linha por linha)
    markup.add(btn_compra, btn_recarga)
    markup.add(btn_trocas, btn_bin)
    markup.add(btn_nivel)
    
    if user_id == ADMIN_ID:
        btn_admin = types.InlineKeyboardButton("🛠️ Painel Admin", callback_data="painel_admin")
        markup.add(btn_admin)
        
    bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "compra_aleatoria":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🛒 **Compra Aleatória:** Nenhum card disponível no momento.")
        
    elif call.data == "recarga":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("R$ 20", callback_data="rec_20"),
            types.InlineKeyboardButton("R$ 30", callback_data="rec_30")
        )
        markup.add(
            types.InlineKeyboardButton("R$ 50", callback_data="rec_50"),
            types.InlineKeyboardButton("R$ 100", callback_data="rec_100")
        )
        markup.add(types.InlineKeyboardButton("Outro Valor", callback_data="rec_outro"))
        
        bot.send_message(call.message.chat.id, "💳 Escolha o valor da recarga (Mínimo R$ 20,00):", reply_markup=markup)
        
    elif call.data.startswith("rec_"):
        bot.answer_callback_query(call.id)
        valor = call.data.split("_")[1]
        if valor == "outro":
            bot.send_message(call.message.chat.id, "Por favor, digite o valor desejado (mínimo R$ 20,00):")
        else:
            bot.send_message(call.message.chat.id, f"Gerando Chave Pix para recarga de R$ {valor},00...")

    elif call.data == "trocas":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🔄 **Área de Trocas e Testador:** Envie o voucher/card para testar se está Live ou Die.")

    elif call.data == "consultar_bin":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🔍 Envie os primeiros 6 números (BIN) para consultar.")

    elif call.data == "consultar_nivel":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⭐ Seus benefícios por Nível:\n- Classic\n- Standard\n- Gold\n- Platinum\n- Black\n- Infinite")

    elif call.data == "painel_admin":
        if call.from_user.id == ADMIN_ID:
            bot.answer_callback_query(call.id)
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("📦 Adicionar Cards", callback_data="adm_add_cards"),
                types.InlineKeyboardButton("📊 Consultar Estoque", callback_data="adm_estoque")
            )
            markup.add(
                types.InlineKeyboardButton("🔑 Configurar Pix", callback_data="adm_pix"),
                types.InlineKeyboardButton("🚫 Bloquear/Desbloquear", callback_data="adm_bloquear")
            )
            bot.send_message(call.message.chat.id, "🛠️ **Painel Administrativo:**", reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "Acesso negado!", show_alert=True)

if __name__ == "__main__":
    print("Bot rodando...")
    bot.infinity_polling()
