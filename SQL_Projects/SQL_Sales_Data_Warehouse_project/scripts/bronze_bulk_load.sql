bulk insert bronze.crm_cust_info
from 'D:\sql-data-warehouse-project\datasets\source_crm\cust_info.csv'
with(
	FIRSTROW = 2,
	fieldterminator = ',',
	tablock
);

select count(*) from bronze.crm_cust_info;
go

bulk insert bronze.crm_prd_info
from 'D:\sql-data-warehouse-project\datasets\source_crm\prd_info.csv'
with(
	FIRSTROW = 2,
	fieldterminator = ',',
	tablock
);

select * from bronze.crm_prd_info

bulk insert bronze.crm_sales_details
from 'D:\sql-data-warehouse-project\datasets\source_crm\sales_details.csv'
with(
	FIRSTROW = 2,
	fieldterminator = ',',
	tablock
);
go

select * from bronze.crm_sales_details

bulk insert bronze.erp_cust_az12
from 'D:\sql-data-warehouse-project\datasets\source_erp\cust_az12.csv'
with(
	FIRSTROW = 2,
	fieldterminator = ',',
	tablock
);

select * from bronze.erp_cust_az12

bulk insert bronze.erp_loc_a101
from 'D:\sql-data-warehouse-project\datasets\source_erp\loc_a101.csv'
with(
	FIRSTROW = 2,
	fieldterminator = ',',
	tablock
);

select * from bronze.erp_loc_a101

bulk insert bronze.erp_px_cat_g1v2
from 'D:\sql-data-warehouse-project\datasets\source_erp\px_cat_g1v2.csv'
with(
	FIRSTROW = 2,
	fieldterminator = ',',
	tablock
);

select * from bronze.erp_px_cat_g1v2
