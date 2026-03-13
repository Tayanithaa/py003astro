"""
AstroGuy AI — Authentication Blueprint
=======================================
Routes:
  /auth/register   — sign up
  /auth/login      — sign in
  /auth/logout     — sign out
  /auth/profile    — view / edit profile
  /auth/forgot-password   — request reset link token
  /auth/reset-password/<token> — set new password
"""
import os
import secrets
from datetime import datetime, timedelta

from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, session, jsonify)
from flask_login import login_user, logout_user, login_required, current_user

from models import db, User, BirthChart
import json

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ── Helpers ────────────────────────────────────────────────────────────────
def _lang():
    return session.get("language", "en")


# ── Register ───────────────────────────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")
        gender   = request.form.get("gender", "")

        # Validation
        if not name or not email or not password:
            error = "All fields are required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm:
            error = "Passwords do not match."
        elif User.query.filter_by(email=email).first():
            error = "Email already registered. Please log in."
        else:
            user = User(name=name, email=email, gender=gender,
                        language=session.get("language", "en"))
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Welcome to AstroGuy AI! Your cosmic journey begins.", "success")
            return redirect(url_for("dashboard"))

    return render_template("auth/register.html",
                           language=_lang(), error=error)


# ── Login ──────────────────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            user.language = session.get("language", user.language)
            db.session.commit()
            # Restore latest saved chart to session
            latest = (BirthChart.query
                      .filter_by(user_id=user.id)
                      .order_by(BirthChart.created_at.desc())
                      .first())
            if latest and latest.chart_json:
                session["user_chart"]   = json.loads(latest.chart_json)
                session["user_profile"] = {
                    "name": latest.full_name, "dob": latest.dob,
                    "time": latest.birth_time, "place": latest.birth_place,
                    "gender": latest.gender
                }
            next_page = request.args.get("next")
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(next_page or url_for("dashboard"))
        else:
            error = "Invalid email or password."

    return render_template("auth/login.html",
                           language=_lang(), error=error)


# ── Logout ─────────────────────────────────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("user_chart", None)
    session.pop("user_profile", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# ── Profile ────────────────────────────────────────────────────────────────
@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    error = success = None
    charts = (BirthChart.query
              .filter_by(user_id=current_user.id)
              .order_by(BirthChart.created_at.desc())
              .all())

    if request.method == "POST":
        action = request.form.get("action")
        if action == "update_profile":
            name   = request.form.get("name", "").strip()
            gender = request.form.get("gender", "")
            if name:
                current_user.name   = name
                current_user.gender = gender
                db.session.commit()
                success = "Profile updated successfully."
            else:
                error = "Name cannot be empty."

        elif action == "change_password":
            old_pw  = request.form.get("old_password", "")
            new_pw  = request.form.get("new_password", "")
            confirm = request.form.get("confirm_password", "")
            if not current_user.check_password(old_pw):
                error = "Current password is incorrect."
            elif len(new_pw) < 8:
                error = "New password must be at least 8 characters."
            elif new_pw != confirm:
                error = "New passwords do not match."
            else:
                current_user.set_password(new_pw)
                db.session.commit()
                success = "Password changed successfully."

        elif action == "toggle_dark":
            current_user.dark_mode = not current_user.dark_mode
            db.session.commit()
            return jsonify({"dark_mode": current_user.dark_mode})

        elif action == "delete_chart":
            chart_id = request.form.get("chart_id")
            chart = BirthChart.query.filter_by(
                id=chart_id, user_id=current_user.id).first()
            if chart:
                db.session.delete(chart)
                db.session.commit()
                success = "Chart deleted."

    return render_template("auth/profile.html",
                           language=_lang(), user=current_user,
                           charts=charts, error=error, success=success)


# ── Forgot Password ────────────────────────────────────────────────────────
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    message = error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user  = User.query.filter_by(email=email).first()
        # Always show success to prevent user enumeration
        message = "If that email exists, a reset link has been sent."
        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token        = token
            user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            # In production: send email with token
            # For dev: flash the link
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            flash(f"[DEV] Reset link: {reset_url}", "info")

    return render_template("auth/forgot_password.html",
                           language=_lang(), message=message, error=error)


# ── Reset Password ─────────────────────────────────────────────────────────
@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    error = None

    if not user or (user.reset_token_expiry and
                    datetime.utcnow() > user.reset_token_expiry):
        flash("Reset link is invalid or has expired.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_pw  = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")
        if len(new_pw) < 8:
            error = "Password must be at least 8 characters."
        elif new_pw != confirm:
            error = "Passwords do not match."
        else:
            user.set_password(new_pw)
            user.reset_token        = None
            user.reset_token_expiry = None
            db.session.commit()
            flash("Password reset successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html",
                           language=_lang(), token=token, error=error)
