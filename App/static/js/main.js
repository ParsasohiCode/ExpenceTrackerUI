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

    // Helper: Get JWT from cookie
    function getAccessToken() {
      const match = document.cookie.match(/access_token=([^;]+)/);
      return match ? match[1] : null;
    }

    // Render expenses
    async function fetchExpenses() {
      const token = getAccessToken();
      const res = await fetch('/expenses/read_all_expenses', {
        headers: { 'Authorization': token }
      });
      const expenses = await res.json();
      renderExpenses(expenses);
    }

    function renderExpenses(expenses) {
      const list = document.getElementById('expensesList');
      const noMsg = document.getElementById('noExpensesMsg');
      let total = 0;
      list.innerHTML = '';
      if (!expenses || expenses.length === 0) {
        noMsg.style.display = '';
        document.getElementById('totalExpenses').innerHTML = '<i class="fa fa-calculator"></i> Total: $0';
        return;
      }
      noMsg.style.display = 'none';
      expenses.forEach(exp => {
        total += exp.amount;
        const li = document.createElement('li');
        li.className = 'expense-item';
        li.innerHTML = `
          <div class="expense-left">
            <div class="expense-desc">${escapeHtml(exp.title)}</div>
            <div class="expense-description">${escapeHtml(exp.description)}</div>
            <div class="expense-meta">${exp.category} | ${exp.date.split('T')[0]}</div>
          </div>
          <div class="expense-right">
            <span class="expense-amount">$${exp.amount}</span>
            <div class="expense-actions">
              <button class="icon-btn delete" title="Delete" onclick="deleteExpense(${exp.id})"><i class="fa fa-trash"></i></button>
              <button class="icon-btn edit" title="Edit" onclick="openEditModalFromData(${exp.id}, '${escapeHtml(exp.title)}', '${escapeHtml(exp.description)}', ${exp.amount}, '${escapeHtml(exp.category)}', '${exp.date.split('T')[0]}')"><i class="fa fa-pen"></i></button>
            </div>
          </div>
        `;
        list.appendChild(li);
      });
      document.getElementById('totalExpenses').innerHTML = `<i class="fa fa-calculator"></i> Total: $${total}`;
    }

    function escapeHtml(text) {
      return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    }

    window.openEditModalFromData = function(id, title, description, amount, category, date) {
      editingId = id;
      document.getElementById('editTitle').value = title;
      document.getElementById('editDescription').value = description;
      document.getElementById('editAmount').value = amount;
      document.getElementById('editCategory').value = category;
      document.getElementById('editDate').value = date;
      document.getElementById('editModal').classList.add('active');
    };

    async function deleteExpense(id) {
      const token = getAccessToken();
      await fetch(`/expenses/delete_expense/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': token }
      });
      fetchExpenses();
    }

    document.getElementById('addExpenseForm').addEventListener('submit', async function(e) {
      e.preventDefault();
      const token = getAccessToken();
      const form = e.target;
      const data = {
        title: form.title.value,
        description: form.description.value,
        amount: parseInt(form.amount.value),
        date: form.date.value,
        category: form.category.value
      };
      await fetch('/expenses/create_expense', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token
        },
        body: JSON.stringify(data)
      });
      closeAddModal();
      fetchExpenses();
    });

    document.getElementById('editExpenseForm').addEventListener('submit', async function(e) {
      e.preventDefault();
      const token = getAccessToken();
      const form = e.target;
      const data = {
        title: form.title.value,
        description: form.description.value,
        amount: parseInt(form.amount.value),
        date: form.date.value,
        category: form.category.value
      };
      await fetch(`/expenses/update_expense/${editingId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token
        },
        body: JSON.stringify(data)
      });
      closeEditModal();
      fetchExpenses();
    });

    document.getElementById('logoutBtn').addEventListener('click', function() {
      // Remove the access_token cookie by setting it to expire in the past
      document.cookie = 'access_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      window.location.href = '/auth/login';
    });

    document.addEventListener('DOMContentLoaded', fetchExpenses);