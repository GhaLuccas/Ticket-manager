// tickets.js

  async function fetchTickets(searchTerm = '', stateFilter = '') {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          window.location.href = 'login.html'; // Redireciona se não houver token
          return;
        }

        // Constrói a URL com base nos parâmetros
        let url = `http://localhost:8000/tickets/?search_term=${searchTerm}`;
        if (stateFilter) {
          url += `&state=${stateFilter}`;
        }

        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Erro ao carregar tickets');
        }

        const data = await response.json();
        const ticketList = document.getElementById('ticketList');

        // Limpa a lista antes de adicionar novos itens
        ticketList.innerHTML = '';

        data.ticket_list.forEach((ticket) => {
          const li = document.createElement('li');
          li.className = 'list-group-item ticket-item';
          li.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-1">Cliente: ${ticket.client.name}</h6>
                <h6 class="mb-1">Empresa: ${ticket.client.company_name || 'Não cadastrado'}</h6>
                <h6 class="mb-1">Chamado: ${ticket.problem}</h6>
                <small class="text-muted">Autor: ${ticket.author.username}</small>
                <small class="text-muted d-block">Solução: ${ticket.solution || 'Sem solução ainda'}</small>
                <!-- Exibe o status do ticket -->
                <div class="mt-2">
                  <span class="badge ${getStatusClass(ticket.state)}" onclick="changeTicketStatus(${ticket.id}, '${ticket.state}')">${ticket.state}</span>
                </div>
              </div>
              <div>
                <button class="btn btn-sm btn-outline-primary me-2" onclick="viewTicket(${ticket.id})">
                  <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteTicket(${ticket.id})">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          `;
          ticketList.appendChild(li);
        });
      } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao carregar tickets.');
      }
    }
  
  // Função para definir a classe CSS com base no status do ticket
  function getStatusClass(state) {
    switch (state) {
      case 'done':
        return 'bg-success';
      case 'to_fix':
        return 'bg-warning';
      case 'on_going':
        return 'bg-info';
      default:
        return 'bg-secondary';
    }
  }
  
  // Função para visualizar um ticket
  function viewTicket(ticketId) {
    window.location.href = `ticket-details.html?id=${ticketId}`;
  }
  
  // Função para deletar um ticket
  async function deleteTicket(ticketId) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        window.location.href = 'login.html'; // Redireciona se não houver token
        return;
      }
  
      const response = await fetch(`http://localhost:8000/tickets/${ticketId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (!response.ok) {
        throw new Error('Erro ao deletar ticket');
      }
  
      // Recarrega a lista de tickets após deletar
      fetchTickets();
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao deletar ticket.');
    }
  }
  
  // Função para mudar o status do ticket
  async function changeTicketStatus(ticketId, currentState) {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        window.location.href = 'login.html'; // Redireciona se não houver token
        return;
      }
  
      // Define o próximo estado com base no estado atual
      const nextState = getNextState(currentState);
  
      const response = await fetch(`http://localhost:8000/tickets/${ticketId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ state: nextState }),
      });
  
      if (!response.ok) {
        throw new Error('Erro ao atualizar o status do ticket');
      }
  
      // Recarrega a lista de tickets após a atualização
      fetchTickets();
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao atualizar o status do ticket.');
    }
  }
  
  // Função para determinar o próximo estado
  function getNextState(currentState) {
    switch (currentState) {
      case 'on_going':
        return 'to_fix';
      case 'to_fix':
        return 'done';
      case 'done':
        return 'on_going';
      default:
        return 'on_going';
    }
  }
  
  // Função para filtrar tickets por estado
  function filterTicketsByState(state) {
    fetchTickets('', state);
  }
  
  // Event Listeners
  document.addEventListener('DOMContentLoaded', () => {
    // Carrega os tickets ao abrir a página
    fetchTickets();
  
    // Evento para o botão de adicionar ticket
    document.getElementById('addTicketButton').addEventListener('click', () => {
      window.location.href = 'create-ticket.html';
    });
  
    // Evento para o botão de clientes
    document.getElementById('clientsButton').addEventListener('click', () => {
      window.location.href = 'clients.html';
    });
  
    // Evento para o campo de pesquisa
    document.getElementById('searchInput').addEventListener('input', (e) => {
      fetchTickets(e.target.value);
    });
  
    // Evento para o botão de logout
    document.getElementById('logoutButton').addEventListener('click', () => {
      localStorage.removeItem('token');
      window.location.href = 'login.html';
    });
  
    // Evento para o filtro de estado
    document.getElementById('stateFilter').addEventListener('change', (e) => {
      filterTicketsByState(e.target.value);
    });
  });