import React, { useEffect, useState, useCallback } from 'react';
import { Button, Flex, Table, Input, message, Card, Tag, Typography, Tooltip, Space, Statistic, Row, Col } from 'antd';
import { DeleteOutlined, SearchOutlined, MailOutlined, RobotOutlined, FileTextOutlined, FilePdfOutlined, ClockCircleOutlined, CheckCircleOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import type { TableColumnsType } from 'antd';
import ModalComponent from '../modal/ModalComponent';
import { EmailApi } from '../../api/email-api';
import type { EmailStatsResponse } from '../../api/email-api';
import './MainComponent.css';

const { Search } = Input;
const { Title, Text } = Typography;

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

const getTypeIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case 'pdf':
      return <FilePdfOutlined />;
    case 'txt':
      return <FileTextOutlined />;
    default:
      return <MailOutlined />;
  }
};

const getTypeColor = (type: string) => {
  switch (type.toLowerCase()) {
    case 'pdf':
      return 'red';
    case 'txt':
      return 'blue';
    default:
      return 'green';
  }
};

const getClassificationColor = (classification: string) => {
  if (classification?.toLowerCase().includes('produtivo')) {
    return 'success';
  } else if (classification?.toLowerCase().includes('improdutivo')) {
    return 'warning';
  }
  return 'default';
};

const getClassificationIcon = (classification: string) => {
  if (classification?.toLowerCase().includes('produtivo')) {
    return <CheckCircleOutlined />;
  } else if (classification?.toLowerCase().includes('improdutivo')) {
    return <ExclamationCircleOutlined />;
  }
  return <RobotOutlined />;
};

const truncateText = (text: string, maxLength: number = 50) => {
  if (!text) return '-';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

const columns: TableColumnsType<EmailType> = [
  { 
    title: <Space><MailOutlined />Título</Space>, 
    dataIndex: 'email_title', 
    sorter: (a, b) => a.email_title.localeCompare(b.email_title),
    render: (text: string) => (
      <Tooltip title={text}>
        <Text strong style={{ color: '#1890ff' }}>
          {truncateText(text, 30)}
        </Text>
      </Tooltip>
    ),
    width: 200
  },
  { 
    title: <Space><FileTextOutlined />Mensagem</Space>, 
    dataIndex: 'message', 
    sorter: (a, b) => a.message.localeCompare(b.message),
    render: (text: string) => (
      <Tooltip title={text}>
        <Text>{truncateText(text, 40)}</Text>
      </Tooltip>
    ),
    width: 250
  },
  { 
    title: <Space><FileTextOutlined />Tipo</Space>, 
    dataIndex: 'type', 
    sorter: (a, b) => a.type.localeCompare(b.type),
    render: (type: string) => (
      <Tag icon={getTypeIcon(type)} color={getTypeColor(type)}>
        {type}
      </Tag>
    ),
    width: 120
  },
  { 
    title: <Space><RobotOutlined />Classificação IA</Space>, 
    dataIndex: 'ai_classification', 
    sorter: (a, b) => a.ai_classification.localeCompare(b.ai_classification),
    render: (classification: string) => (
      <Tag 
        icon={getClassificationIcon(classification)} 
        color={getClassificationColor(classification)}
      >
        {classification || 'Não classificado'}
      </Tag>
    ),
    width: 150
  },
  { 
    title: <Space><RobotOutlined />Resposta Sugerida</Space>, 
    dataIndex: 'ai_suggested_reply', 
    sorter: (a, b) => a.ai_suggested_reply.localeCompare(b.ai_suggested_reply),
    render: (reply: string) => (
      <Tooltip title={reply}>
        <Text type="secondary" italic>
          {truncateText(reply, 50) || 'Nenhuma sugestão'}
        </Text>
      </Tooltip>
    ),
    width: 300
  },
  { 
    title: <Space><ClockCircleOutlined />Data de Criação</Space>, 
    dataIndex: 'created_at',
    sorter: (a, b) => a.created_at.localeCompare(b.created_at),
    render: (text: string) => {
      if (!text) return <Text type="secondary">-</Text>;
      const date = new Date(text);
      const formattedDate = date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
      return (
        <Tooltip title={`Criado em ${formattedDate}`}>
          <Text type="secondary">{formattedDate}</Text>
        </Tooltip>
      );
    },
    width: 150
  },
];

const emailApi = new EmailApi();

const MainComponent: React.FC = () => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState<EmailType[]>([]);
  const [searchText, setSearchText] = useState('');
  const [searchTimeout, setSearchTimeout] = useState<ReturnType<typeof setTimeout> | null>(null);
  const [stats, setStats] = useState<EmailStatsResponse>({
    total: 0,
    produtivos: 0,
    improdutivos: 0,
    nao_classificados: 0,
    pdf: 0,
    txt: 0,
    texto_puro: 0
  });
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 5,
    total: 0,
    showSizeChanger: true,
    pageSizeOptions: ['5', '10', '20', '50', '100'], 
    showTotal: (total: number, range: number[]) => 
      `${range[0]}-${range[1]} de ${total} itens`,
  });

  const fetchStats = async () => {
    try {
      const statsData = await emailApi.getEmailStats();
      setStats(statsData);
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

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
    fetchStats();
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
    fetchStats();
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
      fetchStats();
      
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
    <div className="main-container">
      {/* Cabeçalho com título */}
      <Card className="main-header-card">
        <Title level={2} className="main-title">
          <MailOutlined style={{ marginRight: '8px' }} />
          Sistema de Processamento de Emails
        </Title>
        <Text type="secondary" className="main-subtitle">
          Análise inteligente de emails com classificação por IA
        </Text>
      </Card>

      {/* Cards de estatísticas */}
      <Row gutter={[16, 16]} className="main-stats-row">
        <Col xs={24} sm={12} md={8} lg={4}>
          <Card>
            <Statistic 
              title="Total de Emails" 
              value={stats.total} 
              prefix={<MailOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={4}>
          <Card>
            <Statistic 
              title="Produtivos" 
              value={stats.produtivos} 
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={4}>
          <Card>
            <Statistic 
              title="Improdutivos" 
              value={stats.improdutivos} 
              prefix={<ExclamationCircleOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={4}>
          <Card>
            <Statistic 
              title="PDFs" 
              value={stats.pdf} 
              prefix={<FilePdfOutlined style={{ color: '#f5222d' }} />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={4}>
          <Card>
            <Statistic 
              title="TXTs" 
              value={stats.txt} 
              prefix={<FileTextOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8} lg={4}>
          <Card>
            <Statistic 
              title="Texto Puro" 
              value={stats.texto_puro} 
              prefix={<FileTextOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Card principal com a tabela */}
      <Card 
        className="main-table-card"
      >
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
              icon={<DeleteOutlined />}
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
        size="middle"
        rowSelection={{
          selectedRowKeys,
          onChange: onSelectChange,
        }} 
        columns={columns} 
        dataSource={dataSource}
        loading={loading}
        scroll={{ x: 1200 }}
        rowClassName={(_, index) => 
          index % 2 === 0 ? 'table-row-light' : 'table-row-dark'
        }
        pagination={{
          ...pagination,
          onChange: handleTableChange,
          onShowSizeChange: handleTableChange,
          locale: {
            items_per_page: '/ página',
          }
        }}
        locale={{
          emptyText: (
            <div className="empty-state">
              <MailOutlined className="empty-state-icon" />
              <div>
                <Text type="secondary" className="empty-state-title">
                  Nenhum email encontrado
                </Text>
              </div>
              <div className="empty-state-subtitle">
                <Text type="secondary">
                  {searchText ? 'Tente ajustar sua pesquisa' : 'Adicione alguns emails para começar'}
                </Text>
              </div>
            </div>
          )
        }}
      />
        </Flex>
      </Card>
    </div>
  );
};

export default MainComponent;