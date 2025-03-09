CREATE TABLE ThoiTiet (
  id INT PRIMARY KEY IDENTITY(1,1),
  thành_phố NVARCHAR(50),
  mô_tả NVARCHAR(100),
  nhiệt_độ_thấp_nhất FLOAT,
  nhiệt_độ_cao_nhất FLOAT,
  sức_gió FLOAT,
  độ_ẩm INT,
  lượng_mưa FLOAT,
  khả_năng_mưa FLOAT,
  thời_gian DATETIME DEFAULT GETDATE()
);
Select * from ThoiTiet

DELETE FROM ThoiTiet
SELECT * FROM ThoiTiet;

CREATE TABLE ThoiTietHomQua (
  id INT PRIMARY KEY IDENTITY(1,1),
  thành_phố NVARCHAR(50),
  mô_tả NVARCHAR(100),
  nhiệt_độ_thấp_nhất FLOAT,
  nhiệt_độ_cao_nhất FLOAT,
  sức_gió FLOAT,
  độ_ẩm INT,
  lượng_mưa FLOAT,
  khả_năng_mưa FLOAT,
  thời_gian DATETIME DEFAULT GETDATE()
);

Select * from ThoiTietHomQua