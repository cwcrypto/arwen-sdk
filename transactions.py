'''
Courtesy of James Lovejoy from Digital Currency Initiative
'''

'''
Sequence of txs:
​
TX 0:
Inputs:
    any
Outputs:
    CSV output +n blocks
​
TX 1:
Inputs:
    CSV output +n blocks
Outputs:
    CSV output +n blocks
​
TX x:
Inputs:
    CSV output +n blocks
Outputs:
    any 
'''

import hashlib
​
import bitcointx.core.script as script
import bitcointx.core
import bitcointx.rpc
import bitcointx.wallet
import bitcointx
​
def signrawtransactionwithwallet(self, tx):
    hextx = bitcointx.rpc.hexlify(tx.serialize())
    (r, _) = self._rpc_call('signrawtransactionwithwallet', [hextx])
    r['tx'] = bitcointx.core.CTransaction.deserialize(bitcointx.rpc.unhexlify(r['hex']))
    return r['tx']
​
def delay_output_script(privkey, nLockTime):
    opcodes = [nLockTime,
               script.OP_NOP3,
               script.OP_DROP,
               script.OP_DUP,
               script.OP_HASH160,
               bitcointx.core.Hash160(privkey.pub),
               script.OP_EQUALVERIFY,
               script.OP_CHECKSIG]
​
    return script.CScript(opcodes)
​
def to_p2wsh_scriptPubKey(inp_script):
    return script.CScript([script.OP_0, hashlib.sha256(inp_script).digest()])
​
def spend_delay_output_script(privkey, nLockTime, unsigned_tx, n, amount):
    delay_script = delay_output_script(privkey, nLockTime)
    sighash = script.SignatureHash(delay_script, 
                                   unsigned_tx, 
                                   n, 
                                   script.SIGHASH_ALL, 
                                   amount=amount,
                                   sigversion=script.SIGVERSION_WITNESS_V0)
    sig = privkey.sign(sighash) + bytes([script.SIGHASH_ALL])
    return script.CScriptWitness([sig, privkey.pub, delay_script])
​
def generate_first_tx(contended_outpoints, 
                      incentive_delay, 
                      delay_amount,
                      delay_privkey,
                      bitcoin_digester):
    
    inputs = []
    for outpoint in contended_outpoints:
        txid, n = outpoint.split(';')
        op = bitcointx.core.COutPoint(bitcointx.core.lx(txid), int(n))
        inputs.append(bitcointx.core.CTxIn(op, nSequence=0))
​
    secret = bitcointx.wallet.CBitcoinSecret.from_secret_bytes(bytearray.fromhex(delay_privkey))
    output_script = delay_output_script(secret, incentive_delay)
    output = bitcointx.core.CTxOut(delay_amount * bitcointx.core.COIN, 
                                   to_p2wsh_scriptPubKey(output_script))
​
    unsigned_tx = bitcointx.core.CTransaction(inputs, [output], nVersion=2)
​
    signed_tx = signrawtransactionwithwallet(bitcoin_digester, unsigned_tx)
​
    return signed_tx
​
def generate_second_tx(previous_outpoint, 
                       incentive_delay, 
                       delay_amount, 
                       delay_privkey,
                       prevout_amount):
    txid, n = previous_outpoint.split(';')
    op = bitcointx.core.COutPoint(bitcointx.core.lx(txid), int(n))
    inp = bitcointx.core.CTxIn(op, nSequence=incentive_delay)
    secret = bitcointx.wallet.CBitcoinSecret.from_secret_bytes(bytearray.fromhex(delay_privkey))
    
    output_script = delay_output_script(secret, incentive_delay)
    output = bitcointx.core.CTxOut(delay_amount * bitcointx.core.COIN, 
                                   to_p2wsh_scriptPubKey(output_script))
​
    unsigned_tx = bitcointx.core.CTransaction([inp], [output], nVersion=2)
​
    inp_scripthash = spend_delay_output_script(secret, 
                                               incentive_delay, 
                                               unsigned_tx,
                                               int(n),
                                               int(prevout_amount*bitcointx.core.COIN))
​
    inp = bitcointx.core.CTxIn(prevout=op, nSequence=incentive_delay)
​
    txinwit = bitcointx.core.CTxInWitness(inp_scripthash)
    txwit = bitcointx.core.CTxWitness([txinwit])
​
    signed_tx = bitcointx.core.CTransaction([inp], 
                                            [output], 
                                            nVersion=2, 
                                            witness=txwit)
​
    return signed_tx
​
def generate_tx_sequence(contended_outpoints, 
                         total_value, 
                         fee_per_tx, 
                         n_txs, 
                         delay_per_tx, 
                         delay_privkey,
                         bitcoin_digester):
​
    current_amount = total_value - fee_per_tx
    first_tx = generate_first_tx(contended_outpoints, 
                                 delay_per_tx, 
                                 current_amount, 
                                 delay_privkey,
                                 bitcoin_digester)
    
    txs = [first_tx]
​
    for i in range(n_txs-1):
        last_amount = current_amount
        current_amount -= fee_per_tx
        next_tx = generate_second_tx(bitcointx.core.b2lx(txs[-1].GetTxid())+';0', 
                                     delay_per_tx, 
                                     current_amount, 
                                     delay_privkey, 
                                     last_amount)
        txs.append(next_tx)
​
    serialised_txs = []
    for tx in txs:
        serialised_txs.append(bitcointx.core.b2x(tx.serialize()))
​
    return serialised_txs