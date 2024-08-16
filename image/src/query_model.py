import os
import time
import uuid
import boto3
from pydantic import BaseModel, Field
from typing import List, Optional
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("TABLE_NAME")
# Doan code dung de them cac gia tri khi truy van vao database dynamodb


# Định nghĩa mô hình dữ liệu cho truy vấn sử dụng Pydantic
class QueryModel(BaseModel):
    query_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    create_time: int = Field(default_factory=lambda: int(time.time()))
    query_text: str
    answer_text: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    is_complete: bool = False
    
 # Lấy đối tượng bảng DynamoDB từ tên bảng đã định nghĩa
    @classmethod
    def get_table(cls: "QueryModel") -> boto3.resource:
        dynamodb = boto3.resource("dynamodb")
        return dynamodb.Table(TABLE_NAME)

# Chèn hoặc cập nhật một item trong bảng DynamoDB
    def put_item(self):
        item = self.as_ddb_item()
        try:
            response = QueryModel.get_table().put_item(Item=item) # Chuyển đổi đối tượng hiện tại thành định dạng DynamoDB
            print(response)
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            raise e

# Chuyển đổi đối tượng thành một dictionary có thể lưu trữ trong DynamoDB
    def as_ddb_item(self):
        item = {k: v for k, v in self.dict().items() if v is not None}
        return item

# Lấy một item từ DynamoDB dựa trên query_id
    @classmethod
    def get_item(cls: "QueryModel", query_id: str) -> "QueryModel":
        try:
            response = cls.get_table().get_item(Key={"query_id": query_id})
        except ClientError as e:
            print("ClientError", e.response["Error"]["Message"])
            return None

        if "Item" in response:
            item = response["Item"]
            return cls(**item)
        else:
            return None