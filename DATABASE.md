# Database Schema

The database has one table, 'Product', with the following design:

### Database Description
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | VARCHAR(64) | PRIMARY KEY | Product ID |
| name | VARCHAR(128) | NOT NULL | Product Name |
| price | FLOAT | NOT NULL | Product price |
| type | VARCHAR(64) | NOT NULL | Description |
| image | VARCHAR(256) | NOT NULL | URL image link |


The database is authenticated by a secret value stored in the Secret Manager under 'db-name', with the value
matching the actual name of this database, to ensure integrity of credentials.