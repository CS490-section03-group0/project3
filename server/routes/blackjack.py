import json

from flask import request, session, Blueprint
from sqlalchemy.sql import func
from server.utils.blackjack_deck import draw_card, translate_hand, blackjack_total, get_deck_set
from server import db
from server.models import Transaction, Blackjack


blackjack_bp = Blueprint(
    "blackjack_bp",
    __name__,
)

def new_player(user_id):
    return Blackjack.query.filter_by(user_id=user_id).scalar() is None

def valid_balance(user_id):
    total_tickets = (
        db.session.query(func.sum(Transaction.ticket_amount))
        .filter(Transaction.user_id == user_id)
        .scalar()
    )
    if total_tickets is None:
        return False
    return total_tickets >= 500

@blackjack_bp.route("/api/blackjack/play", methods=["GET"])
def play_blackjack():
    try:
        if "user_id" not in session:
            return {"success": False, "message": "User is not suppose to be here"}
        if valid_balance(session["user_id"]) is False:
            return {"success": False, "message": "Client needs at least 500 tickets to play."}
        return {"success": True, "message": "Welcome to Blackjack!"}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@blackjack_bp.route("/api/blackjack/start", methods=["POST"])
def bet_blackjack():
    try:
        data = json.loads(request.data)
        transaction = Transaction(
            user_id=session["user_id"],
            ticket_amount=-data["amount"],
            activity="blackjack",
        )
        db.session.add(transaction)
        deck = get_deck_set()
        if not deck:
            return {"success": False, "message": "Blackjack server is currently facing an problem."\
                " Please try again later."
            }
        card1 = draw_card(deck)
        card2 = draw_card(deck)
        card3 = draw_card(deck)
        card4 = draw_card(deck)
        dealer_hand = [card1, card3]
        player_hand = [card2, card4]
        if new_player(session["user_id"]):
            player_deck = Blackjack(
                user_id=session["user_id"],
                deck=json.dumps(deck),
                player_hand=json.dumps(player_hand),
                dealer_hand=json.dumps(dealer_hand)
            )
            db.session.add(player_deck)
        else:
            player_row = Blackjack.query.filter_by(user_id=session["user_id"]).first()
            player_row.deck = json.dumps(deck)
            player_row.player_hand = json.dumps(player_hand)
            player_row.dealer_hand = json.dumps(dealer_hand)
        db.session.commit()
        client_dealer = translate_hand(dealer_hand)[0:2]
        client_player = translate_hand(player_hand)
        return {
            "success": True,
            "blackjack" : blackjack_total(player_hand) == 21,
            "dealer": client_dealer,
            "player": client_player,
        }
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@blackjack_bp.route("/api/blackjack/playagain", methods=["POST"])
def play_again_blackjack():
    try:
        data = json.loads(request.data)
        transaction = Transaction(
            user_id=session["user_id"],
            ticket_amount=-data["amount"],
            activity="blackjack",
        )
        db.session.add(transaction)
        query = Blackjack.query.filter_by(user_id=session["user_id"]).first()
        deck = json.loads(query.deck)
        card1 = draw_card(deck)
        card2 = draw_card(deck)
        card3 = draw_card(deck)
        card4 = draw_card(deck)
        dealer_hand = [card1, card3]
        player_hand = [card2, card4]
        if len(deck)<200:
            deck = deck + get_deck_set()
        query.deck = json.dumps(deck)
        query.player_hand = json.dumps(player_hand)
        query.dealer_hand = json.dumps(dealer_hand)
        db.session.commit()
        client_dealer = translate_hand(dealer_hand)[0:2]
        client_player = translate_hand(player_hand)
        return {
            "success": True,
            "blackjack" : blackjack_total(player_hand) == 21,
            "dealer": client_dealer,
            "player": client_player,
        }
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@blackjack_bp.route("/api/blackjack/hit", methods=["GET"])
def hit_blackjack():
    query = Blackjack.query.filter_by(user_id=session["user_id"]).first()
    deck = json.loads(query.deck)
    player_hand = json.loads(query.player_hand)
    next_card = draw_card(deck)
    if len(deck)<200:
        deck = deck + get_deck_set()
    player_hand.append(next_card)
    query.deck = json.dumps(deck)
    query.player_hand = json.dumps(player_hand)
    db.session.commit()
    total = blackjack_total(player_hand)
    client_player = translate_hand(player_hand)
    if total > 21:
        return {
            "success": True,
            "bust": True,
            "winner": "Dealer",
            "blackjack": False,
            "player": client_player
        }
    if total == 21:
        return {
            "success": True,
            "bust": False,
            "blackjack" : True,
            "player": client_player,
        }
    return {
        "success": True,
        "bust": False,
        "blackjack": False,
        "player": client_player
        }

@blackjack_bp.route("/api/blackjack/stand", methods=["GET"])
def stand_blackjack():
    query = Blackjack.query.filter_by(user_id=session["user_id"]).first()
    deck = json.loads(query.deck)
    player_hand = json.loads(query.player_hand)
    dealer_hand = json.loads(query.dealer_hand)
    while blackjack_total(dealer_hand) <= 17:
        dealer_hand.append(draw_card(deck))
    if len(deck)<200:
        deck = deck + get_deck_set()
    query.deck = json.dumps(deck)
    query.player_hand = json.dumps(player_hand)
    query.dealer_hand = json.dumps(dealer_hand)

    client_dealer = translate_hand(dealer_hand)
    client_player = translate_hand(player_hand)
    dealer_total = blackjack_total(dealer_hand)
    player_total = blackjack_total(player_hand)
    if dealer_total > 21 or dealer_total < player_total:
        last_transaction = session.query(Transaction)\
            .filter_by(Transaction.user_id==session["user_id"])\
            .order_by(Transaction.id.desc()).first()
        new_amount = last_transaction.ticket_amount * 1.5
        transaction = Transaction(
            user_id=session["user_id"],
            ticket_amount=new_amount,
            activity="blackjack",
        )
        db.session.add(transaction)
        db.session.commit()
        return {
            "success": True,
            "winner": "player",
            "dealer": client_dealer,
            "player": client_player,
        }
    if dealer_total == player_total:
        return {
            "success": True,
            "winner": "none",
            "dealer": client_dealer,
            "player": client_player,
        }
    return {
        "success": True,
        "winner": "dealer",
        "dealer": client_dealer,
        "player": client_player,
    }

@blackjack_bp.route("/api/blackjack/tiebreaker", methods=["GET"])
def tiebreaker_blackjack():
    query = Blackjack.query.filter_by(user_id=session["user_id"]).first()
    deck = json.loads(query.deck)
    card1 = draw_card(deck)
    card2 = draw_card(deck)
    card3 = draw_card(deck)
    card4 = draw_card(deck)
    dealer_hand = [card1, card3]
    player_hand = [card2, card4]
    if len(deck)<200:
        deck = deck + get_deck_set()
    query.deck = json.dumps(deck)
    query.player_hand = json.dumps(player_hand)
    query.dealer_hand = json.dumps(dealer_hand)
    db.session.commit()
    client_dealer = translate_hand(dealer_hand)[0:2]
    client_player = translate_hand(player_hand)
    return {
        "success": True,
        "blackjack" : blackjack_total(player_hand) == 21,
        "dealer": client_dealer,
        "player": client_player,
    }
