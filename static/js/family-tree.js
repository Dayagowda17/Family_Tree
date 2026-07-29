// Family Tree page interactivity: click-to-view modal, zoom/pan, collapse, search
(function () {
    'use strict';

    function escapeHtml(str) {
        if (str === null || str === undefined) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    document.addEventListener('DOMContentLoaded', function () {
        initMemberModal();
        initCollapseToggles();
        initZoomControls();
        initTreeSearch();
    });

    // ---------- Member detail modal ----------
    function initMemberModal() {
        const modalEl = document.getElementById('memberModal');
        const modalContent = document.getElementById('memberModalContent');
        if (!modalEl || !modalContent || typeof bootstrap === 'undefined') return;

        const bsModal = new bootstrap.Modal(modalEl);

        function renderLoading() {
            modalContent.innerHTML =
                '<div class="modal-body text-center py-5">' +
                '<div class="spinner-border text-primary" role="status"></div>' +
                '</div>';
        }

        function renderError(message) {
            modalContent.innerHTML =
                '<div class="modal-header">' +
                '<h5 class="modal-title">Unable to load member</h5>' +
                '<button type="button" class="btn-close" data-bs-dismiss="modal"></button>' +
                '</div>' +
                '<div class="modal-body"><p class="text-danger mb-0">' + escapeHtml(message) + '</p></div>';
        }

        function relationRow(label, rel, iconClass) {
            if (!rel) return '';
            return '<li class="list-group-item"><i class="bi ' + iconClass + '"></i> ' + label + ': ' +
                '<a href="#" class="member-modal-link" data-member-id="' + rel.id + '">' + escapeHtml(rel.name) + '</a></li>';
        }

        function renderMember(data) {
            const initials = (data.first_name ? data.first_name[0] : '') + (data.last_name ? data.last_name[0] : '');
            const genderClass = (data.gender || 'other').toLowerCase();

            const photoHtml = data.photo_url
                ? '<img src="' + data.photo_url + '" class="img-fluid rounded member-modal-photo" alt="' + escapeHtml(data.full_name) + '">'
                : '<div class="member-modal-avatar avatar-' + genderClass + '">' + escapeHtml(initials.toUpperCase()) + '</div>';

            const childrenHtml = (data.children && data.children.length)
                ? data.children.map(function (c) {
                    return '<li class="list-group-item"><i class="bi bi-person-fill text-success"></i> Child: ' +
                        '<a href="#" class="member-modal-link" data-member-id="' + c.id + '">' + escapeHtml(c.name) + '</a></li>';
                }).join('')
                : '<li class="list-group-item text-muted">No children recorded</li>';

            const fatherRow = relationRow('Father', data.father, 'bi-person-fill text-primary');
            const motherRow = relationRow('Mother', data.mother, 'bi-person-fill text-danger');
            const spouseRow = relationRow('Spouse', data.spouse, 'bi-heart-fill text-danger');

            modalContent.innerHTML =
                '<div class="modal-header">' +
                    '<h5 class="modal-title">' + escapeHtml(data.full_name) + '</h5>' +
                    '<button type="button" class="btn-close" data-bs-dismiss="modal"></button>' +
                '</div>' +
                '<div class="modal-body">' +
                    '<div class="row g-4">' +
                        '<div class="col-md-4 text-center">' +
                            photoHtml +
                            '<div class="mt-3 text-start small">' +
                                '<p class="mb-1"><strong>Gender:</strong> ' + escapeHtml(data.gender || 'N/A') + '</p>' +
                                '<p class="mb-1"><strong>Age:</strong> ' + (data.age !== null && data.age !== undefined ? data.age + ' years old' : 'Not specified') + '</p>' +
                                (data.dob_display ? '<p class="mb-1"><strong>Born:</strong> ' + escapeHtml(data.dob_display) + '</p>' : '') +
                                (data.phone ? '<p class="mb-1"><strong>Phone:</strong> <a href="tel:' + escapeHtml(data.phone) + '">' + escapeHtml(data.phone) + '</a></p>' : '') +
                                (data.email ? '<p class="mb-1"><strong>Email:</strong> <a href="mailto:' + escapeHtml(data.email) + '">' + escapeHtml(data.email) + '</a></p>' : '') +
                                (data.address ? '<p class="mb-0"><strong>Address:</strong> ' + escapeHtml(data.address) + '</p>' : '') +
                            '</div>' +
                        '</div>' +
                        '<div class="col-md-8">' +
                            (data.biography ? '<h6>Biography</h6><p>' + escapeHtml(data.biography) + '</p><hr>' : '') +
                            '<div class="row">' +
                                '<div class="col-sm-6">' +
                                    '<h6 class="mb-2">Parents</h6>' +
                                    '<ul class="list-group list-group-flush mb-3">' +
                                        (fatherRow || '<li class="list-group-item text-muted">No father recorded</li>') +
                                        (motherRow || '<li class="list-group-item text-muted">No mother recorded</li>') +
                                    '</ul>' +
                                '</div>' +
                                '<div class="col-sm-6">' +
                                    '<h6 class="mb-2">Spouse &amp; Children</h6>' +
                                    '<ul class="list-group list-group-flush mb-3">' +
                                        (spouseRow || '') +
                                        childrenHtml +
                                    '</ul>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="modal-footer">' +
                    '<a href="' + data.edit_url + '" class="btn btn-warning"><i class="bi bi-pencil"></i> Edit</a>' +
                    '<a href="' + data.profile_url + '" class="btn btn-primary"><i class="bi bi-box-arrow-up-right"></i> Full Profile Page</a>' +
                    '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>' +
                '</div>';
        }

        function openMemberModal(memberId) {
            if (!memberId) return;
            renderLoading();
            bsModal.show();
            fetch('/family/api/member/' + encodeURIComponent(memberId))
                .then(function (res) {
                    if (!res.ok) {
                        return res.json().then(function (err) {
                            throw new Error(err.error || 'Could not load this member.');
                        }).catch(function () {
                            throw new Error('Could not load this member.');
                        });
                    }
                    return res.json();
                })
                .then(renderMember)
                .catch(function (err) {
                    renderError(err.message);
                });
        }

        document.querySelectorAll('.member-card').forEach(function (card) {
            card.addEventListener('click', function () {
                openMemberModal(card.getAttribute('data-member-id'));
            });
            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    openMemberModal(card.getAttribute('data-member-id'));
                }
            });
        });

        modalContent.addEventListener('click', function (e) {
            const link = e.target.closest('.member-modal-link');
            if (link) {
                e.preventDefault();
                openMemberModal(link.getAttribute('data-member-id'));
            }
        });
    }

    // ---------- Collapse / expand branches ----------
    function initCollapseToggles() {
        document.querySelectorAll('.collapse-toggle').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                const li = btn.closest('li');
                if (!li) return;
                const childUl = li.querySelector(':scope > ul');
                if (!childUl) return;

                const isCollapsed = li.classList.toggle('branch-collapsed');
                childUl.style.display = isCollapsed ? 'none' : '';
                btn.innerHTML = isCollapsed ? '&plus;' : '&minus;';
                btn.title = isCollapsed ? 'Expand this branch' : 'Collapse this branch';
            });
        });
    }

    // ---------- Zoom controls ----------
    function initZoomControls() {
        const treeEl = document.getElementById('family-tree');
        const zoomIn = document.getElementById('zoom-in');
        const zoomOut = document.getElementById('zoom-out');
        const zoomReset = document.getElementById('zoom-reset');
        if (!treeEl) return;

        let scale = 1;
        const MIN_SCALE = 0.4;
        const MAX_SCALE = 1.8;
        const STEP = 0.1;

        function applyScale() {
            treeEl.style.transform = 'scale(' + scale.toFixed(2) + ')';
        }

        if (zoomIn) zoomIn.addEventListener('click', function () {
            scale = Math.min(MAX_SCALE, scale + STEP);
            applyScale();
        });
        if (zoomOut) zoomOut.addEventListener('click', function () {
            scale = Math.max(MIN_SCALE, scale - STEP);
            applyScale();
        });
        if (zoomReset) zoomReset.addEventListener('click', function () {
            scale = 1;
            applyScale();
        });

        const viewport = document.getElementById('tree-viewport');
        if (viewport) {
            viewport.addEventListener('wheel', function (e) {
                if (!e.ctrlKey) return;
                e.preventDefault();
                scale = e.deltaY < 0
                    ? Math.min(MAX_SCALE, scale + STEP)
                    : Math.max(MIN_SCALE, scale - STEP);
                applyScale();
            }, { passive: false });
        }
    }

    // ---------- Search / find a member ----------
    function initTreeSearch() {
        const input = document.getElementById('tree-search');
        if (!input) return;

        function runSearch() {
            const query = input.value.trim().toLowerCase();
            const cards = document.querySelectorAll('.member-card');
            const boxes = document.querySelectorAll('.box');
            let firstMatch = null;

            cards.forEach(function (card) {
                const name = card.getAttribute('data-member-name') || '';
                const isMatch = query.length > 0 && name.indexOf(query) !== -1;
                card.classList.toggle('search-match', isMatch);
                if (isMatch && !firstMatch) firstMatch = card;
            });

            boxes.forEach(function (box) {
                const hasMatch = !!box.querySelector('.member-card.search-match');
                box.classList.toggle('dimmed', query.length > 0 && !hasMatch);
            });

            if (firstMatch) {
                // Make sure any collapsed ancestor branches are expanded so the match is visible
                let li = firstMatch.closest('li');
                while (li) {
                    if (li.classList.contains('branch-collapsed')) {
                        const toggle = li.querySelector(':scope > .box > .collapse-toggle');
                        if (toggle) toggle.click();
                    }
                    li = li.parentElement ? li.parentElement.closest('li') : null;
                }
                firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
            }
        }

        const debounced = typeof debounce === 'function' ? debounce(runSearch, 200) : runSearch;
        input.addEventListener('input', debounced);
    }
})();
