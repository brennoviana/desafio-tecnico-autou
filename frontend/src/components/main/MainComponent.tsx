import React, { useEffect, useState } from 'react';
import { Button, Flex, Table } from 'antd';
import type { TableColumnsType, TableProps } from 'antd';
import ModalComponent from '../modal/ModalComponent';
import { EmailApi } from '../../api/email-api';
import type { EmailResponse } from '../../api/email-api';

type TableRowSelection<T extends object = object> = TableProps<T>['rowSelection'];

interface EmailType {
  id: string;
  email_title: string;
  message: string;
  type: string;
  ai_classification: string;
  ai_suggested_reply: string;
  createdAt: string;
}

const columns: TableColumnsType<EmailType> = [
  { title: 'Título', dataIndex: 'email_title' },
  { title: 'Mensagem', dataIndex: 'message' },
  { title: 'Tipo', dataIndex: 'type' },
  { title: 'Classificação', dataIndex: 'ai_classification' },
  { title: 'Resposta Sugerida', dataIndex: 'ai_suggested_reply' },
  { title: 'Criado Em', dataIndex: 'createdAt' },
];

const MainComponent: React.FC = () => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [loading, setLoading] = useState(false);
  const [dataSource, setDataSource] = useState<EmailType[]>([]);

  const fetchData = async () => {
    const emailApi = new EmailApi();
    const data = await emailApi.getEmails(0, 10);
    setDataSource(data.submissions);
  };

  useEffect(() => {
    fetchData();
  }, []);


  const start = () => {
    setLoading(true);
    setTimeout(() => {
      setSelectedRowKeys([]);
      setLoading(false);
    }, 1000);
  };

  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    console.log('selectedRowKeys changed: ', newSelectedRowKeys);
    setSelectedRowKeys(newSelectedRowKeys);
  };

  const rowSelection: TableRowSelection<EmailType> = {
    selectedRowKeys,
    onChange: onSelectChange,
  };

  const hasSelected = selectedRowKeys.length > 0;

  return (
    <Flex gap="middle" vertical>
      <Flex align="center" gap="middle">
        {hasSelected ? (
          <Button type="primary" onClick={start} disabled={!hasSelected} loading={loading}>
            Delete
          </Button>
          ) : (
            <ModalComponent />
        )}
        {hasSelected ? `Selected ${selectedRowKeys.length} items` : null}
      </Flex>
      <Table<EmailType> rowSelection={rowSelection} columns={columns} dataSource={dataSource} />
    </Flex>
  );
};

export default MainComponent;