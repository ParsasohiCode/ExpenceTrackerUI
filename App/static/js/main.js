document.querySelector('.dashboard-container').classList.add('show');
    // Filter Modal
    function openFilterModal() {
      document.getElementById('filterModal').classList.add('active');
    }
    function closeFilterModal() {
      document.getElementById('filterModal').classList.remove('active');
    }
    document.getElementById('filterModal').addEventListener('click', function(e) { if (e.target === this) closeFilterModal(); });
    // Add Modal
    function openAddModal() {
      document.getElementById('addModal').classList.add('active');
    }
    function closeAddModal() {
      document.getElementById('addModal').classList.remove('active');
    }
    document.getElementById('addModal').addEventListener('click', function(e) { if (e.target === this) closeAddModal(); });
    // Edit Modal
    let editingId = null;
    function handleEditClick(btn) {
      openEditModal(
        btn.getAttribute('data-id'),
        btn.getAttribute('data-title'),
        btn.getAttribute('data-description'),
        btn.getAttribute('data-amount'),
        btn.getAttribute('data-category'),
        btn.getAttribute('data-date')
      );
    }
    function openEditModal(id, title, description, amount, category, date) {
      editingId = id;
      document.getElementById('editTitle').value = title;
      document.getElementById('editDescription').value = description;
      document.getElementById('editAmount').value = amount;
      document.getElementById('editCategory').value = category;
      document.getElementById('editDate').value = date;
      document.getElementById('editExpenseForm').action = `/dashboard/update_expense/${id}`;
      document.getElementById('editModal').classList.add('active');
    }
    function closeEditModal() {
      document.getElementById('editModal').classList.remove('active');
    }
    document.getElementById('editModal').addEventListener('click', function(e) { if (e.target === this) closeEditModal(); });