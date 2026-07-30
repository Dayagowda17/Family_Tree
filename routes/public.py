from flask import Blueprint, render_template, abort
from models.user import User
from models.family import FamilyMember
from routes.family import build_family_tree

public_bp = Blueprint('public', __name__, url_prefix='/public')


@public_bp.route('/<share_token>')
def public_tree(share_token):
    """Read-only family tree for external users - no login required"""
    owner = User.query.filter_by(share_token=share_token).first_or_404()
    members = FamilyMember.query.filter_by(user_id=owner.id).all()
    tree_data = build_family_tree(members)
    return render_template(
        'public_tree.html',
        tree=tree_data,
        members=members,
        owner=owner,
        share_token=share_token
    )


@public_bp.route('/<share_token>/member/<int:member_id>')
def public_member(share_token, member_id):
    """Read-only profile for a single family member - no login required"""
    owner = User.query.filter_by(share_token=share_token).first_or_404()
    member = FamilyMember.query.get_or_404(member_id)

    if member.user_id != owner.id:
        abort(404)

    children = member.get_children()
    return render_template(
        'public_profile.html',
        member=member,
        children=children,
        owner=owner,
        share_token=share_token
    )
