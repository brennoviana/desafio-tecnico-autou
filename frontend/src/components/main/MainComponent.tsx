import React, { useEffect, useState, useCallback } from 'react';
import { Button, Flex, Table, Input, message } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import type { TableColumnsType } from 'antd';
import ModalComponent from '../modal/ModalComponent';
import { EmailApi } from '../../api/email-api';

const { Search } = Input;

interface EmailType {
  id: number;
  email_title: string;
  message: string;
  type: string;
  ai_classification: string;
  ai_suggested_reply: string;
  created_at: string;
  key?: number;
}

const columns: TableColumnsType<EmailType> = [
  { title: 'Título', dataIndex: 'email_title', sorter: (a, b) => a.email_title.localeCompare(b.email_title) },
  { title: 'Mensagem', dataIndex: 'message', sorter: (a, b) => a.message.localeCompare(b.message) },
  { title: 'Tipo', dataIndex: 'type', sorter: (a, b) => a.type.localeCompare(b.type) },
  { title: 'Classificação', dataIndex: 'ai_classification', sorter: (a, b) => a.ai_classification.localeCompare(b.ai_classification) },
  { title: 'Resposta Sugerida', dataIndex: 'ai_suggested_reply', sorter: (a, b) => a.ai_suggested_reply.localeCompare(b.ai_suggested_reply) },
  { 
    title: 'Criado Em', 
    dataIndex: 'created_at',
    sorter: (a, b) => a.created_at.localeCompare(b.created_at),
    render: (text: string) => {
      if (!text) return '-';
      return new Date(text).toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },
];

const emailApi = new EmailApi();

const MainComponent: React.FC = () => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState<EmailType[]>([]);
  const [searchText, setSearchText] = useState('');
  const [searchTimeout, setSearchTimeout] = useState<ReturnType<typeof setTimeout> | null>(null);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 5,
    total: 0,
    showSizeChanger: true,
    pageSizeOptions: ['5', '10', '20', '50', '100'], 
    showTotal: (total: number, range: number[]) => 
      `${range[0]}-${range[1]} de ${total} itens`,
  });

  const fetchData = async (page: number = 1, pageSize: number = 5, searchTitle: string = '') => {
    setLoading(true);
    try {
      const skip = (page - 1) * pageSize;
      let data;
      
      if (searchTitle.trim()) {
        data = await emailApi.searchEmails(skip, pageSize, searchTitle);
      } else {
        data = await emailApi.getEmails(skip, pageSize);
      }
      
      const dataWithKeys = data.submissions.map((item: EmailType) => ({
        ...item,
        key: item.id
      }));
      
      setDataSource(dataWithKeys);
      setPagination(prev => ({
        ...prev,
        current: page,
        pageSize: pageSize,
        total: data.total
      }));
    } catch (error) {
      message.error('Erro ao carregar emails');
    } finally {
      setLoading(false);
    }
  };

  const handleEmailAdded = () => {
    fetchData(pagination.current, pagination.pageSize, searchText);
  };

  const debouncedSearch = useCallback((value: string) => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }

    const newTimeout = setTimeout(() => {
      setSearchText(value);
      setPagination(prev => ({ ...prev, current: 1 }));
      fetchData(1, pagination.pageSize, value);
    }, 500);

    setSearchTimeout(newTimeout);
  }, [searchTimeout, pagination.pageSize]);

  const handleSearch = (value: string) => {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
      setSearchTimeout(null);
    }
    setSearchText(value);
    setPagination(prev => ({ ...prev, current: 1 }));
    fetchData(1, pagination.pageSize, value);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    
    if (!value.trim()) {
      if (searchTimeout) {
        clearTimeout(searchTimeout);
        setSearchTimeout(null);
      }
      handleSearch('');
    } else {
      debouncedSearch(value);
    }
  };

  const handleTableChange = (page: number, pageSize: number) => {
    fetchData(page, pageSize, searchText);
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    return () => {
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
    };
  }, [searchTimeout]);

  const deleteEmails = async () => {
    if (selectedRowKeys.length === 0) return;
    
    setLoading(true);
    try {
      const selectedIds = selectedRowKeys.map(key => Number(key));
      
      const result = await emailApi.deleteEmails(selectedIds);
      
      if (result.deleted_count > 0) {
        message.success(`${result.deleted_count} email(s) deletado(s) com sucesso`);
        
        if (result.not_found_ids && result.not_found_ids.length > 0) {
          message.warning(`${result.not_found_ids.length} email(s) não encontrado(s)`);
        }
      }
      
      setSelectedRowKeys([]);
      await fetchData(pagination.current, pagination.pageSize, searchText);
      
    } catch (error) {
      message.error('Erro ao deletar emails');
    } finally {
      setLoading(false);
    }
  };

  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    setSelectedRowKeys(newSelectedRowKeys);
  };

  const hasSelected = selectedRowKeys.length > 0;

  return (
    <Flex gap="middle" vertical>
      <Flex align="center" gap="middle" justify="space-between">
        <Flex align="center" gap="middle">
          {hasSelected ? (
            <Button 
              type="primary" 
              danger
              onClick={deleteEmails} 
              disabled={!hasSelected} 
              loading={loading}
            >
              Deletar ({selectedRowKeys.length})
            </Button>
            ) : (
              <ModalComponent onEmailAdded={handleEmailAdded} />
          )}
        </Flex>
        
        <Search
          placeholder="Pesquisar por título do email..."
          allowClear
          enterButton={<SearchOutlined />}
          size="middle"
          style={{ width: 300 }}
          onSearch={handleSearch}
          onChange={handleInputChange}
          loading={loading}
        />
      </Flex>
      
      <Table<EmailType>  
        bordered 
        rowSelection={{
          selectedRowKeys,
          onChange: onSelectChange,
        }} 
        columns={columns} 
        dataSource={dataSource}
        loading={loading}
        pagination={{
          ...pagination,
          onChange: handleTableChange,
          onShowSizeChange: handleTableChange,
          locale: {
            items_per_page: '/ página',
            page: 'página'
          }
        }}
      />
    </Flex>
  );
};

export default MainComponent;