import hashlib # модуль работы с хэш-функциями
import json # любые данные к строке
OWNER = 'Serega'
balance = 50000

my_account = {
    "name": "Serega",
    "balance": balance,
    "open_date": "20-09-2021"
}

# Example
text = 'Hello'
binary = text.encode() #binary date
test_hash = hashlib.sha256(binary).hexdigest() #hexdigest выводит хэш в виде хексстроки


def data_to_hash(data):

    str_account = json.dumps(data, sort_keys = True) #данные в виде строки json format

    binary_data = str_account.encode() #binary

    return hashlib.sha256(binary_data).hexdigest()[:10] # Хэш структуры данных (первые 10 символов)

def is_valid_hash(hash):
    return hash[0:2] == '00'

# проверка хэша в правильном формате
def is_valid_proof(block, proof): #подходит ли число(proof)
    block_copy = block.copy()
    block_copy["proof"] = proof
    hash = data_to_hash(block_copy) # Новый хэш с новой частью информации
    valid_hash = is_valid_hash(hash)
    return valid_hash # hash starting with 00?

# Имитация майнинга, необходимо число добавление которого дает 00 в начале хэша
def mine_proof_of_work(block):
    proof = 0
    while not is_valid_proof(block, proof):
        proof += 1
    return proof

genesis_block = {
    "from": "", # sender
    "to":"", # reciever
    "amount": 0.0,
    # "proof": 0,
    # "prev_hash": "empty",
} # 1st block empty
genesis_block["proof"] = mine_proof_of_work(genesis_block)

# в блокчейне всегда есть первый Genesys блок
blockchain = [
    genesis_block, # 1st block empty
] # blockchain - transaction list

def add_new_block(account_from, account_to, amount): # функция добавления блока в блокчейн
    prev_block = blockchain[-1] #последний элемент
    prev_block_hash = data_to_hash(prev_block)
    block = {
        "from": account_from,
        "to": account_to,
        "amount": amount,
        "prev_hash": prev_block_hash
    } #block creation
    proof = mine_proof_of_work(block) # block mining
    block["proof"] = proof
    blockchain.append(block) # block added to blockchain

add_new_block(OWNER, "Billy", 1300)
add_new_block(OWNER, "Marina", 300)
add_new_block(OWNER, "Dmitriy", 737)
add_new_block(OWNER, "Dasha", 300)

add_new_block("Billy", "Marina", 150)
add_new_block("Marina", "Dasha", 250)
add_new_block("Dasha", "Dmitriy", 3)
add_new_block("Dmitriy", "Dasha", 250)

# 1. Переделываем функцию add_new_block, 
# чтобы при добавлении блока использовалась функция майнинга
# 2. Переписываем validate_blockchain, чтобы проверяла начало с нулей
# 3. Посчитаем балансы всех участников
# Один вариант
def how_much_money(name):
    money = 0
    for block in blockchain:
        if name == block['to']:
            money += block['amount']
        if name == block['from']:
            money -= block['amount']
    print(f'На данный момент у {name} баланс - {money}')

# Так как нет ключей-считаем по именам
def calculate_balance():
    balances = {} # Все балансы
    for block in blockchain:
        if block["from"] in balances:
            balance_from = balances[block["from"]]
        else:
            balance_from = 0
        
        if block["to"] in balances:
            balance_to = balances[block["to"]]
        else:
            balance_to = 0

        balance_from -= block["amount"]
        balance_to += block["amount"]

        balances[block["from"]] = balance_from
        balances[block["to"]] = balance_to
    return balances        

# calculate_balance()
# подсчитать баланс на текущий момент, при валидации транзакции в функции validate_blockchain
# Мы в ней проверяем совпадение хэшей, надо проверить что amount в каждой транзакции каждого блока доступен пользователю(кроме Serega)

def validate_blockchain(): # функция проверки хэшей(блокчейна)
    prev_block = None

    for block in blockchain:

        res = '' # обратная связь по транзакции
        if prev_block:
            balances = calculate_balance() # расчет всех балансов на текущий момент

            if block['from'] == OWNER: 
                res = "Владелец блокчейна может иметь любой баланс."
            else:
                if block['from'] in balances:
                    if block['amount'] <= balances[block['from']]:
                        res = 'Ok' # если сумма перевода меньше или равна сумме на балансе
                    else:
                        res = 'Сумма перевода превышает сумму на счете.'
            print('Transaction:', block)
            print('Actual balances:', balances)
            print(res)

            # сверяем хэш
            actual_prev_hash = data_to_hash(prev_block) # hash previous
            recorded_prev_hash = block["prev_hash"]
            if not is_valid_hash(actual_prev_hash):
                print(f'Blockchain is invalid, proof of work - invalid')
            if actual_prev_hash != recorded_prev_hash:
                print(f"Blockchain is ivalid, expected hash {recorded_prev_hash}, actual hash {actual_prev_hash}")
            print(f'Valid hash {recorded_prev_hash}')
        
        prev_block = block

print(blockchain)
validate_blockchain()
'''
# Искуственный взлом, коллизия
block = 5
amount = blockchain[block]["amount"]
expected_hash = blockchain[block+1]["prev_hash"] #необходимость совпадения хэша
hash = ""
while hash != expected_hash:
    amount +=1 # Увеличиваем размер транзакции
    blockchain[block]["amount"] = amount №записываем в блокчейн новую сумму
    hash = data_to_hash(blockchain[block]) #считаем хэш заново
# мы подменили сумму перевода, но хэши совпали
'''

# Вместо обычной функции date_to_hash, используем функцию майнинга mine_proof...
'''
# Было:
block = blockchain[5]
print ('_________Было_________')
print(block, data_to_hash(block))
#Стало
block = blockchain[5].copy()
block["proof"] = mine_proof_of_work(block)
print ('_________Стало_________')
print(block, data_to_hash(block))
'''
