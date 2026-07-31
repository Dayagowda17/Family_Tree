from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask import jsonify
from flask_login import login_required, current_user
from models import db
from models.family import FamilyMember
from datetime import datetime, date
from auth_decorators import admin_required

family_bp = Blueprint('family', __name__, url_prefix='/family')


@family_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_member():
    """Add a new family member - Admin only"""
    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            gender = request.form.get('gender', '').strip()
            
            if not first_name or not last_name or not gender:
                flash('First name, last name, and gender are required', 'danger')
                return redirect(url_for('family.add_member'))
            
            member = FamilyMember(
                user_id=current_user.id,
                first_name=first_name,
                last_name=last_name,
                gender=gender
            )
            
            # Optional fields
            dob_str = request.form.get('dob')
            if dob_str:
                try:
                    member.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except:
                    pass
            
            member.phone = request.form.get('phone', '').strip() or None
            member.email = request.form.get('email', '').strip() or None
            member.address = request.form.get('address', '').strip() or None
            member.biography = request.form.get('biography', '').strip() or None
            
            # Family relationships
            father_id = request.form.get('father_id')
            mother_id = request.form.get('mother_id')
            spouse_id = request.form.get('spouse_id')
            
            if father_id and father_id != '':
                member.father_id = int(father_id)
            if mother_id and mother_id != '':
                member.mother_id = int(mother_id)
            if spouse_id and spouse_id != '':
                member.spouse_id = int(spouse_id)
            
            db.session.add(member)
            db.session.commit()
            
            flash(f'{first_name} {last_name} added successfully!', 'success')
            return redirect(url_for('family.view_member', member_id=member.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding member: {str(e)}', 'danger')
            return redirect(url_for('family.add_member'))
    
    # Get available family members for relationships
    members = FamilyMember.query.filter_by(user_id=current_user.id).all()
    return render_template('add_member.html', members=members)


@family_bp.route('/<int:member_id>')
@login_required
def view_member(member_id):
    """View a family member's profile - All users can view"""
    member = FamilyMember.query.get_or_404(member_id)
    
    # Check if current user owns this member
    if member.user_id != current_user.id:
        flash('You do not have permission to view this member', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    children = member.get_children()
    return render_template('profile.html', member=member, children=children)


@family_bp.route('/api/member/<int:member_id>')
@login_required
def member_detail_api(member_id):
    """Return full details for a single member as JSON - All users can access
    Used by the family-tree 'click a name' modal so the whole tree page stays 
    intuitive and in-place (no full page reload needed)."""
    member = FamilyMember.query.get_or_404(member_id)

    if member.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to view this member'}), 403

    children = member.get_children()

    data = member.to_dict()
    data['full_name'] = member.get_full_name()
    data['age'] = member.get_age()
    data['dob_display'] = member.dob.strftime('%B %d, %Y') if member.dob else None
    data['photo_url'] = url_for('static', filename='uploads/' + member.photo) if member.photo else None
    data['father'] = {'id': member.father.id, 'name': member.father.get_full_name()} if member.father else None
    data['mother'] = {'id': member.mother.id, 'name': member.mother.get_full_name()} if member.mother else None
    data['spouse'] = {'id': member.spouse.id, 'name': member.spouse.get_full_name()} if member.spouse else None
    data['children'] = [{'id': c.id, 'name': c.get_full_name()} for c in children]
    data['profile_url'] = url_for('family.view_member', member_id=member.id)
    
    # Only include edit URL if user is admin
    if current_user.is_admin():
        data['edit_url'] = url_for('family.edit_member', member_id=member.id)
    
    return jsonify(data)


@family_bp.route('/<int:member_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_member(member_id):
    """Edit a family member - Admin only"""
    member = FamilyMember.query.get_or_404(member_id)
    
    if member.user_id != current_user.id:
        flash('You do not have permission to edit this member', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        try:
            member.first_name = request.form.get('first_name', '').strip()
            member.last_name = request.form.get('last_name', '').strip()
            member.gender = request.form.get('gender', '').strip()
            
            dob_str = request.form.get('dob')
            if dob_str:
                try:
                    member.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except:
                    pass
            
            member.phone = request.form.get('phone', '').strip() or None
            member.email = request.form.get('email', '').strip() or None
            member.address = request.form.get('address', '').strip() or None
            member.biography = request.form.get('biography', '').strip() or None
            
            # Family relationships
            father_id = request.form.get('father_id')
            mother_id = request.form.get('mother_id')
            spouse_id = request.form.get('spouse_id')
            
            member.father_id = int(father_id) if father_id and father_id != '' else None
            member.mother_id = int(mother_id) if mother_id and mother_id != '' else None
            member.spouse_id = int(spouse_id) if spouse_id and spouse_id != '' else None
            
            db.session.commit()
            flash(f'{member.first_name} {member.last_name} updated successfully!', 'success')
            return redirect(url_for('family.view_member', member_id=member.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating member: {str(e)}', 'danger')
    
    members = FamilyMember.query.filter_by(user_id=current_user.id).all()
    return render_template('edit_member.html', member=member, members=members)


@family_bp.route('/<int:member_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_member(member_id):
    """Delete a family member - Admin only"""
    member = FamilyMember.query.get_or_404(member_id)
    
    if member.user_id != current_user.id:
        flash('You do not have permission to delete this member', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    name = f"{member.first_name} {member.last_name}"
    
    try:
        db.session.delete(member)
        db.session.commit()
        flash(f'{name} has been deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting member: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard.dashboard'))


def _group_age_key(group):
    """Return the earliest (oldest) date of birth among a group's members.
    Groups/members without a dob are treated as the youngest so they sort last."""
    dobs = [m.dob for m in group['members'] if m.dob]
    if dobs:
        return min(dobs)
    return date.max


def build_family_tree(members):
    member_by_id = {member.id: member for member in members}
    group_by_member = {}
    groups = {}

    # Infer co-parent groups from children: if a child has both father_id and mother_id,
    # group those two parents together as a couple node (even if spouse relation isn't stored).
    for child in members:
        fid = child.father_id
        mid = child.mother_id
        if fid and mid and fid in member_by_id and mid in member_by_id:
            a, b = (fid, mid) if fid < mid else (mid, fid)
            group_key = f"{a}-{b}"
            groups.setdefault(group_key, {'members': [], 'children': set(), 'parents': set()})
            # we'll store ids here; dedupe later
            groups[group_key]['members'].extend([a, b])
            group_by_member[a] = group_key
            group_by_member[b] = group_key

    # Also group spouses if a spouse_id exists (one-sided allowed).
    # Only create a spouse group when neither partner is already part of another group.
    for member in members:
        sid = member.spouse_id
        if member.id not in group_by_member and sid and sid in member_by_id and sid not in group_by_member:
            a, b = (member.id, sid) if member.id < sid else (sid, member.id)
            group_key = f"{a}-{b}"
            groups.setdefault(group_key, {'members': [], 'children': set(), 'parents': set()})
            if a not in groups[group_key]['members']:
                groups[group_key]['members'].append(a)
            if b not in groups[group_key]['members']:
                groups[group_key]['members'].append(b)
            group_by_member[a] = group_key
            group_by_member[b] = group_key

    # Create single-member groups for any member not part of a co-parent group
    for member in members:
        if member.id not in group_by_member:
            group_key = f"{member.id}"
            groups.setdefault(group_key, {'members': [], 'children': set(), 'parents': set()})
            groups[group_key]['members'].append(member.id)
            group_by_member[member.id] = group_key

    # Clean group members (unique, sorted by name) and replace ids with member objects
    for key, group in list(groups.items()):
        unique_ids = []
        seen = set()
        for mid in group['members']:
            if mid not in seen:
                seen.add(mid)
                unique_ids.append(mid)
        # convert ids to member objects and sort
        members_sorted = sorted(
            [member_by_id[i] for i in unique_ids],
            key=lambda x: (x.dob if x.dob else date.max, x.last_name or '', x.first_name or '')
        )
        groups[key]['members'] = members_sorted

    # Build parent-child group relationships: each child belongs to its own group; parents' groups link to child's group
    for child in members:
        child_group = group_by_member.get(child.id)
        parent_groups = set()
        for parent_id in (child.father_id, child.mother_id):
            if parent_id and parent_id in group_by_member:
                parent_groups.add(group_by_member[parent_id])
        for pg in parent_groups:
            if pg != child_group:
                groups[pg]['children'].add(child_group)
                groups[child_group]['parents'].add(pg)

    def make_group_node(group_key, root=False, visited=None):
        # Prevent infinite recursion by tracking visited group keys (cycle detection)
        if visited is None:
            visited = set()
        if group_key in visited:
            return None
        visited.add(group_key)

        group = groups[group_key]
        label = ' & '.join(f"{m.first_name} {m.last_name}" for m in group['members'])
        if root:
            css_class = 'root'
        elif len(group['members']) == 2:
            css_class = 'couple'
        else:
            css_class = 'child'

        children_keys = sorted(group['children'], key=lambda key: _group_age_key(groups[key]))
        children_nodes = []
        for child_key in children_keys:
            if child_key in visited:
                # skip to avoid cycles
                continue
            node = make_group_node(child_key, root=False, visited=set(visited))
            if node:
                children_nodes.append(node)

        # include member dicts so template can render links
        member_dicts = [{
            'id': m.id,
            'first_name': m.first_name,
            'last_name': m.last_name,
            'gender': m.gender,
            'photo': m.photo
        } for m in group['members']]

        return {
            'label': label,
            'css_class': css_class,
            'members': member_dicts,
            'children': children_nodes
        }

    root_keys = [key for key, group in groups.items() if not group['parents']]
    root_keys = sorted(root_keys, key=lambda key: _group_age_key(groups[key]))
    return [make_group_node(root_key, root=True if i == 0 else False) for i, root_key in enumerate(root_keys)]


@family_bp.route('/tree')
@login_required
def family_tree():
    """View the family tree - All users can view"""
    members = FamilyMember.query.filter_by(user_id=current_user.id).all()
    tree_data = build_family_tree(members)

    family_name = current_user.family_name
    if not family_name and members:
        last_names = [m.last_name.strip() for m in members if m.last_name and m.last_name.strip()]
        if last_names:
            # Group case-insensitively so "KS" and "ks" count as the same surname
            counts = {}
            for ln in last_names:
                key = ln.lower()
                counts.setdefault(key, {'count': 0, 'display': ln})
                counts[key]['count'] += 1
                # Prefer an ALL-CAPS or Title-Case version for display if we see one
                if ln.isupper() or (ln[0].isupper() and not counts[key]['display'][0].isupper()):
                    counts[key]['display'] = ln
            best_key = max(counts, key=lambda k: counts[k]['count'])
            family_name = counts[best_key]['display']

    return render_template('family_tree.html', tree=tree_data, members=members,
                            family_name=family_name, is_admin=current_user.is_admin())


@family_bp.route('/tree_debug')
@login_required
def family_tree_debug():
    """Return JSON with groups, mappings and tree for debugging - All users can access"""
    members = FamilyMember.query.filter_by(user_id=current_user.id).all()

    # Recreate groups similarly to build_family_tree for debugging
    member_by_id = {member.id: member for member in members}
    group_by_member = {}
    groups = {}

    for member in members:
        spouse_id = member.spouse_id
        if spouse_id and spouse_id in member_by_id and member.id < spouse_id:
            spouse = member_by_id[spouse_id]
            if spouse.spouse_id == member.id:
                group_key = f"{member.id}-{spouse_id}"
                groups.setdefault(group_key, {'members': [], 'parents': set(), 'children': set()})
                groups[group_key]['members'].append(member.id)
                groups[group_key]['members'].append(spouse.id)
                group_by_member[member.id] = group_key
                group_by_member[spouse.id] = group_key

    for member in members:
        if member.id not in group_by_member:
            group_key = f"{member.id}"
            groups.setdefault(group_key, {'members': [], 'parents': set(), 'children': set()})
            groups[group_key]['members'].append(member.id)
            group_by_member[member.id] = group_key

    for member in members:
        child_group = group_by_member.get(member.id)
        for parent_id in (member.father_id, member.mother_id):
            if parent_id and parent_id in group_by_member:
                parent_group = group_by_member[parent_id]
                if parent_group != child_group:
                    groups[parent_group]['children'].add(child_group)
                    groups[child_group]['parents'].add(parent_group)

    # Serialize sets to lists for JSON
    groups_serialized = {k: {'members': v['members'], 'parents': list(v['parents']), 'children': list(v['children'])} for k, v in groups.items()}

    tree = build_family_tree(members)
    return jsonify({'groups': groups_serialized, 'group_by_member': group_by_member, 'tree': tree})
