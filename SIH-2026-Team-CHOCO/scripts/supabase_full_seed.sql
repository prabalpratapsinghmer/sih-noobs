-- Auto-generated comprehensive dataset for SIH26184 Supabase Cloud
BEGIN;

        CREATE TEMP TABLE temp_officers AS
        SELECT user_id, username FROM users;
    

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0001', '7edbb159-a8f6-43d4-9980-be8ab8e66ac1', 28500, '2026-09-03 09:32:49'::timestamp, 'UPI_FRAUD', 'scammer1@okhdfc',
                   '+919839958838', '\xb22fb84e74c549ea73e5705a89b630496df260400487f52f132886bbbdeda8aaf80f4ba5922b'::bytea, 'HDFC Bank', 'TXN26184000001',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-09-03 09:32:49'::timestamp, '2026-09-03 09:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('7edbb159-a8f6-43d4-9980-be8ab8e66ac1', 'CMP-20260905-0001', '\x1c3d51975e1452c6ee860350851d6cf5fa9784a506a8c9951a0dbf41be781ba26374abf00a095189fea329a2'::bytea, '\x9ddd24e489273d4d86608e54faa1cc264c2b336fef3eb3aaf67e69233731d5f81e0cde21a9920fb73b'::bytea,
                    'victim1@example.gov.in', '12 Cyber Park, Mumbai', '\x481bc0ca8be9093632f82e424c971e51675c961ec3731798da96391674bc7f2c97f067efc4d3abeed1aa8cfefd41965b'::bytea,
                    'victim1@upi', '2026-09-03 09:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0002', 'cdf47420-53c5-4f9b-9697-489e25825246', 15000, '2026-08-28 12:32:49'::timestamp, 'UPI_FRAUD', 'scammer2@okhdfc',
                   '+919841227216', '\x1f20fdde372b6f452524f9db5a772c13dbe63253c9943fe66856ac56d2597d2f708c5a78cb7f'::bytea, 'HDFC Bank', 'TXN26184000002',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-28 12:32:49'::timestamp, '2026-08-28 12:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('cdf47420-53c5-4f9b-9697-489e25825246', 'CMP-20260905-0002', '\x7d0803fe5e752a0ac42c1dee7e2f01338e26f2a460bc1062f9e1a1c107ab8427e11609126b852b3e308da7a9'::bytea, '\xc9e5410cbfeb13281aa8a747e682f19c7684e921007a69c3d6efbf03b6a8a7b6d4aa774ac80d8669a0'::bytea,
                    'victim2@example.gov.in', '24 Cyber Park, Mumbai', '\xac8089fbdb06bebcaaa52433dd0ae9cd639f7338c97a42b550a5ac456f77e211125360e5c29d0fbb855f5371195dd505'::bytea,
                    'victim2@upi', '2026-08-28 12:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0003', '647acb58-4901-4bdc-8447-bbe573b40e2d', 500000, '2026-08-24 23:32:49'::timestamp, 'LOAN_APP_FRAUD', 'scammer3@okstate',
                   '+919831429110', '\xb6c47e7c554d5e38fe5fe292250c3c1e1197c655becc57faa9fd8e0bb37842791b90ecfb2539'::bytea, 'State Bank of India', 'TXN26184000003',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-08-24 23:32:49'::timestamp, '2026-08-24 23:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('647acb58-4901-4bdc-8447-bbe573b40e2d', 'CMP-20260905-0003', '\xbc34f75376dd4177f010e1283978ce9686b67d401aeebcca2bf86ac3043e9eb5170aeb922d6abc16155c7fdd'::bytea, '\x571034b4f24035b2c5110d34e73a2b1c6651d80092032324e7b6de9173d9eb537bb17bf9e4e1c8fa16'::bytea,
                    'victim3@example.gov.in', '36 Cyber Park, Mumbai', '\x087ae380235052d198d73d3ac2752c13adc97922f7453d1f966ef1c76d8c02b56bca1ad54689524a6ca444f7fca7f565ae4a417f75aeab59f21c'::bytea,
                    'victim3@upi', '2026-08-24 23:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0004', '35a166cc-19e5-4447-bb5c-a379a097f849', 180000, '2026-08-31 01:32:49'::timestamp, 'UPI_FRAUD', 'scammer4@okaxis',
                   '+919822981052', '\xd851ab5b3375b13d5b7949111f2f25fabfd97176b70de8587b1dda66debecc5afdbab7338c72'::bytea, 'Axis Bank', 'TXN26184000004',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-31 01:32:49'::timestamp, '2026-08-31 01:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('35a166cc-19e5-4447-bb5c-a379a097f849', 'CMP-20260905-0004', '\xf2018ad8d2968dcb806135a7557a70aef8a3cade59fa6fbf9723385ea8db196da4b5f40ef235d00543e0226b'::bytea, '\x09a052c68f1de2548fdde2591b28e079c8fb801d860043e0fa24af56cf7c245eb25606af88d3cef999'::bytea,
                    'victim4@example.gov.in', '48 Cyber Park, Mumbai', '\x51106828149f0f57e94fdec4ba36bf4f7b40f4ff5a47efbec3ea7956f588b52c47e83cf7bc3db379db99d84012ef1e3b'::bytea,
                    'victim4@upi', '2026-08-31 01:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0005', '233b4114-f02e-4c83-a939-a11384975f1c', 950000, '2026-09-01 01:32:49'::timestamp, 'UPI_FRAUD', 'scammer5@okstate',
                   '+919884093639', '\x96fd6d3fc6b259034a0d854ed9e20b55447affa5911a7a98925b5fd4128a92ab616985252e63'::bytea, 'State Bank of India', 'TXN26184000005',
                   'RESOLVED'::complaintstatus, user_id, '2026-09-01 01:32:49'::timestamp, '2026-09-01 01:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('233b4114-f02e-4c83-a939-a11384975f1c', 'CMP-20260905-0005', '\xec91d0461f4dd476e74e126ea7dd4f63bde91545a3f590d4cac76fbd0003f3aa7399579d15a2932aeb3398eb'::bytea, '\x4f69b4d92a876e5ab6316440b414e098871e5437d2a5ab5ffa677ea0759964d211d795471db17dc623'::bytea,
                    'victim5@example.gov.in', '60 Cyber Park, Mumbai', '\x48a487e2c8ec4444eab94ed986217a79d69ecf1b518a4787fb94e6d02c00fffd3b1e7059c23862736ad1aec72703c537c77e48dd4f22ee71ecfb'::bytea,
                    'victim5@upi', '2026-09-01 01:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0006', 'ed02bf7a-2f34-4cc9-8d4f-809466ac948a', 120000, '2026-08-31 22:32:49'::timestamp, 'UPI_FRAUD', 'scammer6@okstate',
                   '+919861019678', '\xfa5d7265c790bbb9c93ccfe065e477dc291c53a966acd385ae09ec4aea0052d7da2ce3be6233'::bytea, 'State Bank of India', 'TXN26184000006',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-31 22:32:49'::timestamp, '2026-08-31 22:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('ed02bf7a-2f34-4cc9-8d4f-809466ac948a', 'CMP-20260905-0006', '\x79aa9be5af16f54a40cf42b2d421d0788db867e8442e1d91708c1c0ec55a54bcdd3bd5424111a6309763cc6a'::bytea, '\x005ba3f3467ebfa52545a31493c35923f133db055d16f9d5bb568a85992e1a79a9f8a799dea36b9665'::bytea,
                    'victim6@example.gov.in', '72 Cyber Park, Mumbai', '\x92311a2e46ac9ed074c0c8d198c2da46161120721ae608d6a45e5a238316aa1a5d4a07fe7e0d95e04d51ce5c36eac93f9840299684808ce8118d'::bytea,
                    'victim6@upi', '2026-08-31 22:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0007', 'bd18d3ee-7818-4f64-b9be-9332c3e6b3a9', 180000, '2026-08-25 10:32:49'::timestamp, 'TASK_SCAM', 'scammer7@okkotak',
                   '+919845833156', '\x99db5725a41b5a837fad05b481ca2be394c799bb8c077543b78d4d803ae91e6dae3631ad5697'::bytea, 'Kotak Mahindra Bank', 'TXN26184000007',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-25 10:32:49'::timestamp, '2026-08-25 10:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('bd18d3ee-7818-4f64-b9be-9332c3e6b3a9', 'CMP-20260905-0007', '\x11bcd5b94cbc36b7067f071b8e7544c182c4c8aff1bca89812d472b096bc15201f408b7e181842d688c11ab4'::bytea, '\xd9fb3f0db2026aa749eb333638376984ec7abbe3aeaefe793ea9fc330624e0f9e0c55bd1a0da1c83ff'::bytea,
                    'victim7@example.gov.in', '84 Cyber Park, Mumbai', '\xb346105d43e9ad34c4b8154d5f07d90024280b53d0c143e26f8dc704f8ad29f8d632bceda8865e1b8fcd13a470f26cbb418b8a50d76a8961bd80'::bytea,
                    'victim7@upi', '2026-08-25 10:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0008', '60d567f2-8595-4aab-b41c-9b24643b5274', 85000, '2026-08-21 19:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer8@okaxis',
                   '+919846231783', '\x0c26f7e9bd91537d1c27c667baf51c51a919292a2d7bdd26b9bd8db6ca9f2576e978117ff2e5'::bytea, 'Axis Bank', 'TXN26184000008',
                   'RESOLVED'::complaintstatus, user_id, '2026-08-21 19:32:49'::timestamp, '2026-08-21 19:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('60d567f2-8595-4aab-b41c-9b24643b5274', 'CMP-20260905-0008', '\x540af8ac8842250a1825b96027a707758ddd97278898297eee2c637c09ff74eb97f03b6e0ceba8f3df9a5f93'::bytea, '\xc700944cb7665eb0bc18345db777342302271dfdc8148023b547684bde6f82de99c4d864927d6ab8b9'::bytea,
                    'victim8@example.gov.in', '96 Cyber Park, Mumbai', '\x2eded2f464181717aed184599fb11deadc7806e30d90f7b1d866b3b47b659a94c0dbd0a227f1dc61750617d3bfac9c01'::bytea,
                    'victim8@upi', '2026-08-21 19:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0009', '68be7ab3-d330-4f05-bfd7-652fb1dcc622', 85000, '2026-09-01 10:32:49'::timestamp, 'INVESTMENT_SCAM', 'scammer9@okicici',
                   '+919863843426', '\x2a0716007736b7b94c795b4514cf220249ec5adcc53e5453d5baf5a07db9ffa5b937a2adb2d9'::bytea, 'ICICI Bank', 'TXN26184000009',
                   'SUBMITTED'::complaintstatus, user_id, '2026-09-01 10:32:49'::timestamp, '2026-09-01 10:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('68be7ab3-d330-4f05-bfd7-652fb1dcc622', 'CMP-20260905-0009', '\x0dd33b944b549556f37f4076a759905143d809998c60c948a5f3835e4565989f7fcaa4b5ecbbf876a50950cd'::bytea, '\xe6e030f8ab70c7687ef0c193e412747593dbfa9a828222db622da84f83e7b83281764838ef837c92cc'::bytea,
                    'victim9@example.gov.in', '108 Cyber Park, Mumbai', '\x9ffa8e0b01d633862dbf013fccd3c0b42be66dcf4c8546c6830fce34c1945cf53c972b85f12060fa78ee9d55dea8951078'::bytea,
                    'victim9@upi', '2026-09-01 10:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0010', '9b81680e-408e-4366-9bd6-6728126697a5', 500000, '2026-09-03 05:32:49'::timestamp, 'ELECTRICITY_BILL', 'scammer10@okhdfc',
                   '+919845551614', '\x2dca8d92e1fd16a8f158453d16b00e11c6a2ad4ceb691b74897716007dda6912baf979702761'::bytea, 'HDFC Bank', 'TXN26184000010',
                   'RESOLVED'::complaintstatus, user_id, '2026-09-03 05:32:49'::timestamp, '2026-09-03 05:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('9b81680e-408e-4366-9bd6-6728126697a5', 'CMP-20260905-0010', '\xbdc4f4a016900d0a01be845c24d565d253f2775c4b2eb7fecc6fac69ee1cd5847a8a5184182a3b50b440ef66fd'::bytea, '\xf7b7d6f165e156a6e7db58d442be6693cdffd4e277fedb1b1d0cbaa214ac8cc6ed0404fd7fc278fc54'::bytea,
                    'victim10@example.gov.in', '120 Cyber Park, Mumbai', '\x71e82f5732a6e91137cdde99986c75cd379a8d10901836b7b7fa1147805ac64df485e0804114fcc497c8e7df1b11e251'::bytea,
                    'victim10@upi', '2026-09-03 05:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0011', '1c3ff6b6-fc46-4bec-8039-bc7615cef0d1', 350000, '2026-08-29 10:32:49'::timestamp, 'TASK_SCAM', 'scammer11@okhdfc',
                   '+919878387461', '\x96b9906d2590c9125dcdc017ba92de077020f8122162db31aa2b51277a087037d3d12d5c9020'::bytea, 'HDFC Bank', 'TXN26184000011',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-29 10:32:49'::timestamp, '2026-08-29 10:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('1c3ff6b6-fc46-4bec-8039-bc7615cef0d1', 'CMP-20260905-0011', '\xe15b118ad48fd4837f863830d3d69e7f79af0dcadc25b7fc749e5cedbaedf8f204955f5df02e2d719253bbd1af'::bytea, '\x3a31388067501de7fd7bd8eed0348ee1dd2e0906e2bc8e59d22466303b3a1c97ce12982e760d940e9f'::bytea,
                    'victim11@example.gov.in', '132 Cyber Park, Mumbai', '\xc3c4ece2b341f181e031a16ca10ca3627817b4894d845694c921a55fb0e19145182215933719e133b9e7fae68ad5a058'::bytea,
                    'victim11@upi', '2026-08-29 10:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0012', '41e9549d-546e-4cdd-b64f-c56347201eb5', 45000, '2026-08-30 00:32:49'::timestamp, 'INVESTMENT_SCAM', 'scammer0@okpunjab',
                   '+919818526544', '\x624aa2da1eaee9bda0837accf3effe0c9f7b9e37cf97ed56507ba38c23acc868f5545f112840'::bytea, 'Punjab National Bank', 'TXN26184000012',
                   'RESOLVED'::complaintstatus, user_id, '2026-08-30 00:32:49'::timestamp, '2026-08-30 00:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('41e9549d-546e-4cdd-b64f-c56347201eb5', 'CMP-20260905-0012', '\xeda8b5917ee47ca145a7e3879dbc5af277f6661dacb947d496ee1b8251a3d61315cb7b3ec07b4944bf5255268f'::bytea, '\x735a75b7e467a7a7d242bd6eb736fa09eab73f35c0b905328e3c9867d8974b812e5dafc72faca19792'::bytea,
                    'victim12@example.gov.in', '144 Cyber Park, Mumbai', '\xf5f498cd2a95fb180ef0bffb5633550258a7c45fd1b531e296da39a4607cc6574bfbd0d019124ffbe5bb263ff805bea407b9dbb8ba5194dad38d94'::bytea,
                    'victim12@upi', '2026-08-30 00:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0013', '9833ddd9-70e4-48f6-a6bd-16234b701e03', 120000, '2026-08-25 19:32:49'::timestamp, 'LOAN_APP_FRAUD', 'scammer1@okkotak',
                   '+919825374874', '\x56f5a8e4f485f1c8fd148537926ee891cc29e62383475de56b4f63a8e6fe7e6519144b74cadc'::bytea, 'Kotak Mahindra Bank', 'TXN26184000013',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-25 19:32:49'::timestamp, '2026-08-25 19:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('9833ddd9-70e4-48f6-a6bd-16234b701e03', 'CMP-20260905-0013', '\x26e6841d6800e5763ecee5b16da8d9983da89a2591cebe06bb077bb32f020cb834e57f32f556265d6139e95b02'::bytea, '\x9ce99d4eaa3c74910ae3fb892723b5983e0f527d26c0a536e59c4bcb66afa802a8720962dcc5cc8733'::bytea,
                    'victim13@example.gov.in', '156 Cyber Park, Mumbai', '\x54c997f40c90f08eda8e732173417936a1f81726a421a75f520b3c5fa279d6e9763f4a053bd886d85e92a561328b0e94d607fa0e97c07830b6b1'::bytea,
                    'victim13@upi', '2026-08-25 19:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0014', '22255f3e-3ed9-4c06-87d3-05b95b46be80', 350000, '2026-08-28 07:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer2@okstate',
                   '+919845351479', '\x61e0dd798d5087ff9038fc7311a35b037c2f10f255572f55d4299383a22a727f02f95fc5bdc7'::bytea, 'State Bank of India', 'TXN26184000014',
                   'RESOLVED'::complaintstatus, user_id, '2026-08-28 07:32:49'::timestamp, '2026-08-28 07:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('22255f3e-3ed9-4c06-87d3-05b95b46be80', 'CMP-20260905-0014', '\xdad9a089740bead4b4484d617240bf23486d6eec1fdcf40b89afa81f5f3f2913631c1399d18aa41aa881c21023'::bytea, '\xa1f99d51de746e76d87de220e1a2f4b5049af752d8701c92362227fd2c5d7bd30fcc81b493a11f93b9'::bytea,
                    'victim14@example.gov.in', '168 Cyber Park, Mumbai', '\xc9cc4d47efe12e29f535ebb4dec638f0cffb681794e89a1099d8acb45b1e013eb4ec6cc37005fa1cfb4ddb342d589a6b754891e9e4fb61a75b34'::bytea,
                    'victim14@upi', '2026-08-28 07:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0015', '7adfd5e0-973f-483a-ac0d-69776babe900', 950000, '2026-08-24 07:32:49'::timestamp, 'LOAN_APP_FRAUD', 'scammer3@okhdfc',
                   '+919860185867', '\x463478466ca93394b78a18ec340c4ba8d84376e31159240fef6300a47d5153473261d9b40d4a'::bytea, 'HDFC Bank', 'TXN26184000015',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-24 07:32:49'::timestamp, '2026-08-24 07:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('7adfd5e0-973f-483a-ac0d-69776babe900', 'CMP-20260905-0015', '\x6abf20f11ac3075763fc69c10dcb91b5baa2daaf17f0eeae3aa7df60c07c5fa839e2c08e7d68a7781d46db9867'::bytea, '\x594626059953c8839c9d8a6c948b449ba2ce12151b072da2ce1d38c50922cbb1a0ea8c240ff255e4f0'::bytea,
                    'victim15@example.gov.in', '180 Cyber Park, Mumbai', '\x802abd95f5f9ecc86c3200fadd0f7de1707a007b7246aea87e9ae5946bc2403f95786929bb1699f57eae47726b6d5d71'::bytea,
                    'victim15@upi', '2026-08-24 07:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0016', 'c1b75d4b-2b09-4646-b676-5569bb594cb4', 500000, '2026-09-02 11:32:49'::timestamp, 'UPI_FRAUD', 'scammer4@okicici',
                   '+919851273847', '\xf522d1651aeafcf67928b4f44a2bc18227d020cd9e1841cff8b5b31607d1e0d8517f787b04c0'::bytea, 'ICICI Bank', 'TXN26184000016',
                   'SUBMITTED'::complaintstatus, user_id, '2026-09-02 11:32:49'::timestamp, '2026-09-02 11:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('c1b75d4b-2b09-4646-b676-5569bb594cb4', 'CMP-20260905-0016', '\xe5992d0837d7a727309581fd0f73536304741ac9715d8074238ad31edd96962b4b7f02cec2db7402570d77a0da'::bytea, '\x4d5728ffcf78d046f9fe767576f10f595f71b8a7df6afda4b401d601c69cef462a474bc7b4a0fed3e2'::bytea,
                    'victim16@example.gov.in', '192 Cyber Park, Mumbai', '\xe2456d311e2e3cac5c35450218ce3c404b64ced1c2b131ac98cfa5793c3425473ad5511ba58ff912493137a27eafddb3be'::bytea,
                    'victim16@upi', '2026-09-02 11:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0017', '09835c95-92e6-43f8-9482-f844f3c2fa76', 500000, '2026-09-02 21:32:49'::timestamp, 'INVESTMENT_SCAM', 'scammer5@okpunjab',
                   '+919826879290', '\x927b29301cdec87e1f2cbe50976e12a05bc43d6acd8ff1f783ca0cd6d6fb04ab9c1cd2f47e15'::bytea, 'Punjab National Bank', 'TXN26184000017',
                   'SUBMITTED'::complaintstatus, user_id, '2026-09-02 21:32:49'::timestamp, '2026-09-02 21:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('09835c95-92e6-43f8-9482-f844f3c2fa76', 'CMP-20260905-0017', '\x9b27c6ca41898ac1aafe4a4b6050f69b555ce075a39397d6577f4e42e0d48d4bf59d299150862698595c54d010'::bytea, '\xc696e55f34806193799ae228f16179bdd69fca5178b48757a47906936e6771d1732ff1a5290077b276'::bytea,
                    'victim17@example.gov.in', '204 Cyber Park, Mumbai', '\x0784c0a5151b08ec44d0d97ef56d0373365e49d7d657f4a3717258c43c48be81a83cc4bd2454b095be4a887b33ff426c872d919fe466c73b8a1bb1'::bytea,
                    'victim17@upi', '2026-09-02 21:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0018', 'c03a7f1c-0b08-4245-aab5-6b5f391f1f51', 350000, '2026-08-30 01:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer6@okkotak',
                   '+919851837852', '\xab37ca6bfc20bf3e9a1e1cd96e2426cbc99ae09ea9104f1abff9b60bacbb4b94e460d8428288'::bytea, 'Kotak Mahindra Bank', 'TXN26184000018',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-30 01:32:49'::timestamp, '2026-08-30 01:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('c03a7f1c-0b08-4245-aab5-6b5f391f1f51', 'CMP-20260905-0018', '\x6bf662852d6a9dd46bc9508f314b5e8220590d349fd62a9250efd9078830009f446bf4b99f3400731e1fe86961'::bytea, '\x128b522e6e57bafcefde7adb109308a5769678f43b97a5175761e012fbf01cd4467249c8ce2860de3d'::bytea,
                    'victim18@example.gov.in', '216 Cyber Park, Mumbai', '\x5be15a0f2be11aa0e5556d31cf43ab0d6336698bd4a1782df5e21c86de5f3040880ac93efa2f3a8057313c1fb457c9cb2b72c06f2244528bbf5d'::bytea,
                    'victim18@upi', '2026-08-30 01:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0019', '0b39d896-6201-466d-b8f4-9a07855a170d', 85000, '2026-08-28 05:32:49'::timestamp, 'UPI_FRAUD', 'scammer7@okstate',
                   '+919888961459', '\x467f8cd59fb74039338682124d6edddfdfb28a0988f8170a59e36a7258006b4a9fa9152ea597'::bytea, 'State Bank of India', 'TXN26184000019',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-08-28 05:32:49'::timestamp, '2026-08-28 05:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('0b39d896-6201-466d-b8f4-9a07855a170d', 'CMP-20260905-0019', '\x4d71cc9bc8ce64335c5e8c966940f2c262ced4ca8874eca353ce323df9597de2018b372e84f4201de62987d789'::bytea, '\x0c106dce0788a5371e5660cdd685ed0b71789945f54ae6dfdb6e12d17aedd03bd0feb44c222310e9c2'::bytea,
                    'victim19@example.gov.in', '228 Cyber Park, Mumbai', '\x41b54df62bf9e8fa23feceea517076191e01556bcfcbe39fdca52d06076e470c7d04ea5c7bd50a2a17098a8e2d38204d367b3fac0ca56a13a684'::bytea,
                    'victim19@upi', '2026-08-28 05:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0020', '9d5086a0-100b-475a-92a1-0b09327a8a42', 15000, '2026-09-03 20:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer8@okstate',
                   '+919854349361', '\x8502cbf1112c783e1e8720f800a862a604e949b67679b0fdee20ffe47883e8903e5d5ff0df5d'::bytea, 'State Bank of India', 'TXN26184000020',
                   'SUBMITTED'::complaintstatus, user_id, '2026-09-03 20:32:49'::timestamp, '2026-09-03 20:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('9d5086a0-100b-475a-92a1-0b09327a8a42', 'CMP-20260905-0020', '\x7e2849fb2a8058cd5b65b3f595fb21f153422fe29ef47c162f15303b42a52bc09d531d1898cf77e830892b0410'::bytea, '\x71699daf3fd19d492e1f46aa18ace5c5451504173aa210c84983f0357ea268b05dbc5b79fec0e50ecd'::bytea,
                    'victim20@example.gov.in', '240 Cyber Park, Mumbai', '\xaca7560f3cf9971a9b02469cbcba2ed13fab10a7574eefd928d1dfefb01baf37b793e1545635b4fbcf255733c89a9b6f74c6c7b18589a9d430a5'::bytea,
                    'victim20@upi', '2026-09-03 20:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0021', '0dacd1f0-71ee-4b1b-bd5a-e56a22bc1373', 500000, '2026-09-04 09:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer9@okaxis',
                   '+919835556386', '\xe69357ae73118f5eaaccf42f127a97176cd424235d0251daf82ae1d68147ef737aab3744ab3b'::bytea, 'Axis Bank', 'TXN26184000021',
                   'RESOLVED'::complaintstatus, user_id, '2026-09-04 09:32:49'::timestamp, '2026-09-04 09:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('0dacd1f0-71ee-4b1b-bd5a-e56a22bc1373', 'CMP-20260905-0021', '\x0ac822df0fbbf40b9e858c388b23a46b373c721273e3bc33dd266ac97aa57e1c77f4afd3d9c569177d1f8f89ad'::bytea, '\x8b4ef34abc848cc992ba16ebff0e4bc3b6f3414d03f84071acd82eafebf2aed0d9e8480cff783d62fe'::bytea,
                    'victim21@example.gov.in', '252 Cyber Park, Mumbai', '\xfae69e6cadcbbd7b7ee508b9683b35fe3d9c22c26c835bbb54d822bde0b84f6bbfb8bb59824feaca4b66b91f52772862'::bytea,
                    'victim21@upi', '2026-09-04 09:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0022', '36943ec6-401c-4f10-82f0-fc0e02d33f0c', 350000, '2026-08-26 09:32:49'::timestamp, 'ELECTRICITY_BILL', 'scammer10@okkotak',
                   '+919897705310', '\x29f2ecb633dcd6b16a8e3f05cece214b8894840127a3e82727cc775621f663785e9e1d6205fa'::bytea, 'Kotak Mahindra Bank', 'TXN26184000022',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-26 09:32:49'::timestamp, '2026-08-26 09:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('36943ec6-401c-4f10-82f0-fc0e02d33f0c', 'CMP-20260905-0022', '\xe0b468f72ede10dcc1a32182d8483f6fa90d6d14ff37a7b68b431f20c95f48441c2f6aa9b1539b83846e84b0e2'::bytea, '\xb351a3446deaa4fe535e03b135cd1af00707f1ad7d652cae80aa69c9f8a1648954509867810dae6973'::bytea,
                    'victim22@example.gov.in', '264 Cyber Park, Mumbai', '\x901c11c1c464dd5bf0c31541d62e4e6a46a6ccdcc6bea4970c9e1e3f39f047ecf6ef2aab8f87c604e772b9f9d318faa5c2c83f8adabdfef5421e'::bytea,
                    'victim22@upi', '2026-08-26 09:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0023', '63ca8c69-bd8d-4238-9b31-11b25fc84efc', 85000, '2026-09-03 04:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer11@okhdfc',
                   '+919866623995', '\xa85e40bccc9fb8e3d4d5c9ec905c0876a1a8487958bb93679f5012d6d8395c70bc23cd44765a'::bytea, 'HDFC Bank', 'TXN26184000023',
                   'RESOLVED'::complaintstatus, user_id, '2026-09-03 04:32:49'::timestamp, '2026-09-03 04:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('63ca8c69-bd8d-4238-9b31-11b25fc84efc', 'CMP-20260905-0023', '\x03bb537176b02ade17942f9ed22f2d44db6c4e9ee1cd3d104262bc8d5cffbfe207b79b92dcc9932a5a46b654c6'::bytea, '\x5d027c4e0137b2db18a27830250594e0785b39708c58126348754e01ac1ab3e43d987a3814a58ec12a'::bytea,
                    'victim23@example.gov.in', '276 Cyber Park, Mumbai', '\xdacb84d6a9f9f447d66c0fd535e6f88defeda0a2c7baef3557f17439c8c7b19d056fb85027798c483cdd9a1321617a5d'::bytea,
                    'victim23@upi', '2026-09-03 04:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0024', '950415c0-3611-4877-957a-79a23ed114b9', 950000, '2026-08-23 12:32:49'::timestamp, 'UPI_FRAUD', 'scammer0@okkotak',
                   '+919882556484', '\x24cb20c6a1f5482e41bb0a189a2b6130f17905a079a3f31cfc0588f3583fef10a1596d79b65b'::bytea, 'Kotak Mahindra Bank', 'TXN26184000024',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-23 12:32:49'::timestamp, '2026-08-23 12:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('950415c0-3611-4877-957a-79a23ed114b9', 'CMP-20260905-0024', '\x58295be3e3f0fbdf7c05ca07fc5ecb983452172878ff4cbc11b90241b4310e4b76dac85cca8c924f978c6bca9f'::bytea, '\x49a4f40d22dd6e8ed69ecfd2b4e05214f6afe9adc93c575c31dfe28f0e083c839f2dab4d89022705fd'::bytea,
                    'victim24@example.gov.in', '288 Cyber Park, Mumbai', '\xd236a66b89954623f42c95f2cff617da4661edc54132f77f5354e223a1baef04de125b157e3be634dfb585b3a6f06e7d7b08d44c9c44bbaabe1b'::bytea,
                    'victim24@upi', '2026-08-23 12:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0025', '12072026-ced7-482e-9fec-913c35bc4fce', 350000, '2026-08-22 11:32:49'::timestamp, 'ELECTRICITY_BILL', 'scammer1@okhdfc',
                   '+919863826716', '\xc327fd45546fea783b1743862c46a52859d0b4aca9fef0299c905a8b4e036a40c41d1d38008d'::bytea, 'HDFC Bank', 'TXN26184000025',
                   'RESOLVED'::complaintstatus, user_id, '2026-08-22 11:32:49'::timestamp, '2026-08-22 11:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('12072026-ced7-482e-9fec-913c35bc4fce', 'CMP-20260905-0025', '\xeb9975bab744d6b302d6c96c61ac7123316d714b9414bc87408f2e2c7d9a66ff69fb4e2eab412e8eb58ff35a96'::bytea, '\xa267087a6f4b6baed4ac8d2d26273d5368e5669ca5c5af03a8ad7f8b5f43589af10dd6ab0488322612'::bytea,
                    'victim25@example.gov.in', '300 Cyber Park, Mumbai', '\x04c6d47a41b3fe0a641970a369b30f1f74b1baa4b21985b2419dc49b12ad6b5422d6efc17cba32349f352093344c3a67'::bytea,
                    'victim25@upi', '2026-08-22 11:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0026', '9dcd72ec-9687-4b8f-9a48-b0ec88be89a4', 120000, '2026-08-24 19:32:49'::timestamp, 'INVESTMENT_SCAM', 'scammer2@okicici',
                   '+919866775103', '\xc0629f285bf2726ca4e7b2555330ae499be2f63ff5ae73682a43cf13208703d345698561d32a'::bytea, 'ICICI Bank', 'TXN26184000026',
                   'RESOLVED'::complaintstatus, user_id, '2026-08-24 19:32:49'::timestamp, '2026-08-24 19:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('9dcd72ec-9687-4b8f-9a48-b0ec88be89a4', 'CMP-20260905-0026', '\x5d53577d37bd02330c29769571f90e071ea412d22c7e78e5d66bbe498b715c49eb0e28c88922ec792fad749e96'::bytea, '\x58732196a5843756d405ba82635f7cd7a90448ad1ad40ab5943c915b402fde334d518e9d6052839c19'::bytea,
                    'victim26@example.gov.in', '312 Cyber Park, Mumbai', '\xa6de723b554032db7d8d264286327763d53c08a5c25a6870871d75ae3da641a1937b7ffc6f0a346ac0884eeecc3c54fb07'::bytea,
                    'victim26@upi', '2026-08-24 19:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0027', 'b4ecee96-9f41-4c29-94eb-ef08b91f92b2', 85000, '2026-08-24 19:32:49'::timestamp, 'TASK_SCAM', 'scammer3@okstate',
                   '+919887736262', '\xb7ff16100ca4187bed3f3955e8662a9666fd5251264afefcea0ed20a040b63ef3fea033d1d8b'::bytea, 'State Bank of India', 'TXN26184000027',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-24 19:32:49'::timestamp, '2026-08-24 19:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('b4ecee96-9f41-4c29-94eb-ef08b91f92b2', 'CMP-20260905-0027', '\xa51aeedb4726bba2e87a21298683fbb89a68d311e49ebf6190a8386529322b0d48873dc24bbd7fcef61e598850'::bytea, '\x680f97a97933fcc03d3dd0e16691ccb3ffef9ef8ac37d96a4dd1365a53860bf65f38142761dda3fcb8'::bytea,
                    'victim27@example.gov.in', '324 Cyber Park, Mumbai', '\xb8bf7503ab5e3afa545ac5454468cc2abaa729933cd99028c9e84abc7498c7bd458c7a195807e11151fe577c0a92c60ec1b8dadaf19e2c9a8d0c'::bytea,
                    'victim27@upi', '2026-08-24 19:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0028', '744c3c7e-eb00-460b-aef8-e481def1a671', 15000, '2026-09-03 11:32:49'::timestamp, 'LOAN_APP_FRAUD', 'scammer4@okpunjab',
                   '+919881286543', '\x73d889be5e9aae518450505fd0c6e8381290272d4725719a924bbbfa0a914122915c48ccb2cb'::bytea, 'Punjab National Bank', 'TXN26184000028',
                   'RESOLVED'::complaintstatus, user_id, '2026-09-03 11:32:49'::timestamp, '2026-09-03 11:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('744c3c7e-eb00-460b-aef8-e481def1a671', 'CMP-20260905-0028', '\x517246131e837c08377603a444306b74d74f33eb481919fecfeb1d2ca41882f1b1ab87ebbed7ce06be2e4654e9'::bytea, '\xa8f30b994a93bcf3c9f8d22db1a520195130753da04c2bdaa287f58e6d522fddb66e0ee1d9b0b00fa7'::bytea,
                    'victim28@example.gov.in', '336 Cyber Park, Mumbai', '\xafe2c9c4036f12a2d2f2990a19729af77b4f75c83341066b4954a14dd8a6bc106db94358987dbeb758c94b4826d08203979c2716f6269bc3f7dee1'::bytea,
                    'victim28@upi', '2026-09-03 11:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0029', '97bb216c-d3e7-43d1-91a1-a1799256b4b2', 85000, '2026-08-27 11:32:49'::timestamp, 'ELECTRICITY_BILL', 'scammer5@okpunjab',
                   '+919843046464', '\x9c6651b8528353262a93eb136539dd774834cd42be10a00d04f524cdd6e5ea2bb2dbfcdde270'::bytea, 'Punjab National Bank', 'TXN26184000029',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-27 11:32:49'::timestamp, '2026-08-27 11:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('97bb216c-d3e7-43d1-91a1-a1799256b4b2', 'CMP-20260905-0029', '\x7fd961aaae2648af0d52b8c6c84b5ac06eeb5854b06a11a7b8edb23c68d504673058026c36454e213a9ce09b33'::bytea, '\xb3e953f37ddce5f885f1c6bf1012f4aa63c603c82b8703342bf6bd8bd87a7fb5bb76d77c3f8936b180'::bytea,
                    'victim29@example.gov.in', '348 Cyber Park, Mumbai', '\xcf9c46b790764dd22d8d3a2fb4f4871a11306213199908aadecd700a4f2ca316afc93d56718a882f5bdfe1353395a0efac26e4de1da9072095dad5'::bytea,
                    'victim29@upi', '2026-08-27 11:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0030', '1ba61446-46cc-486e-b2c4-dc10fe8d8bbb', 180000, '2026-09-02 04:32:49'::timestamp, 'TASK_SCAM', 'scammer6@okkotak',
                   '+919852169044', '\xe4720faa29cbb1fdd0c42b10f7495414b28a1ce8618766874d404941a4de910e0c39ae42f598'::bytea, 'Kotak Mahindra Bank', 'TXN26184000030',
                   'ANALYZING'::complaintstatus, user_id, '2026-09-02 04:32:49'::timestamp, '2026-09-02 04:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('1ba61446-46cc-486e-b2c4-dc10fe8d8bbb', 'CMP-20260905-0030', '\xa5e67611f3b469431616d3625c6d86e77be9da3e6e621823e585305126906118731514b78d92ad4dd8992119bc'::bytea, '\x35033644b04d61e1c2166076933d8a7ed77809a315a51f0c0a5b4a913363eaf1f15e2cee8fcbdf168f'::bytea,
                    'victim30@example.gov.in', '360 Cyber Park, Mumbai', '\xfe5e742d04d95b7d413adc89656655cbcf976412092a80285789fd9ecc1911a8895ea21ec0418419bd84178586decc4ae94bddd0eb27e75195d6'::bytea,
                    'victim30@upi', '2026-09-02 04:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0031', '0ee4ecfe-3940-4d40-9314-2457c8d9f5e6', 180000, '2026-08-27 09:32:49'::timestamp, 'INVESTMENT_SCAM', 'scammer7@okstate',
                   '+919871510041', '\xeb2fc7ead1b6cbe47789c28f26f4a141936a366575f7fe799ced998d6c5c3e40b31ed500d928'::bytea, 'State Bank of India', 'TXN26184000031',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-27 09:32:49'::timestamp, '2026-08-27 09:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('0ee4ecfe-3940-4d40-9314-2457c8d9f5e6', 'CMP-20260905-0031', '\x724650c479b9fc6c2367cacba26fd018caa46f9e36dbec09f408bd7f06c7e13e90041e9b66675b6e55c13f97a9'::bytea, '\x8e0c7121d30244195e87e11f00d03f0cca4d005a847bed86c14a8617dbf9745b080c1be306b62da6cf'::bytea,
                    'victim31@example.gov.in', '372 Cyber Park, Mumbai', '\xf063f5add83b4cdb1912dced0a60f1e55adf086d3e8f5147806572b05b6ae12af6f469f79f17e917c32ec905ae08708a3fbfb8565897f9bd9533'::bytea,
                    'victim31@upi', '2026-08-27 09:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0032', 'cfa8a3d1-6f3b-4a4c-88f0-728cfab0e2a9', 120000, '2026-08-31 03:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer8@okstate',
                   '+919842787299', '\xf3ffa7bce40d6a3178822fb408d308f831ced107f2f704193d0e80b7fe27f34382d01439983b'::bytea, 'State Bank of India', 'TXN26184000032',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-08-31 03:32:49'::timestamp, '2026-08-31 03:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('cfa8a3d1-6f3b-4a4c-88f0-728cfab0e2a9', 'CMP-20260905-0032', '\x80b6dca07492ceb0b6fda787c49be9c579e9a85ba49f3b5677997505d3658f7316a799bf2fa26b12ce317fd91c'::bytea, '\x968e17fca79b0b48146737555f06998f85e9614a2951bdf18c40fdd8ff3cff9221024ee3a6401478c3'::bytea,
                    'victim32@example.gov.in', '384 Cyber Park, Mumbai', '\xac396a78764d6507daebd88cb0a265f9fb165630fcd11dcecc2ce836f0e9154b9fb7c907f1f3cf9f81cd41bdc721cbd4917fd27e2356803cd5d1'::bytea,
                    'victim32@upi', '2026-08-31 03:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0033', 'edba179c-e3fd-4a5e-86e1-c2ed405354e8', 28500, '2026-08-24 19:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer9@okstate',
                   '+919824366125', '\xb4ff8406acd188abe67e1b64300d832cd85a34af4d6fb090fc78cd6d46177e9b014980809860'::bytea, 'State Bank of India', 'TXN26184000033',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-08-24 19:32:49'::timestamp, '2026-08-24 19:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('edba179c-e3fd-4a5e-86e1-c2ed405354e8', 'CMP-20260905-0033', '\x8f293e43fdc8925454fbbcbe19f14edf54eece8afecf0f92f44a83999de3018d8f8d9d5ca683dfa5060949f980'::bytea, '\x8abb01571e553e25f06de83691182df413bc923b4e32b08eda3df57305ca1678f69d08de9111b23d8d'::bytea,
                    'victim33@example.gov.in', '396 Cyber Park, Mumbai', '\xaccdcb87fc8c210277376966eb917f5b3f5a8bcecb60429abe0fe5ad55d76770b39c7a42be4d242c85be84a4084da6e2ef8f267fb2e2225d2337'::bytea,
                    'victim33@upi', '2026-08-24 19:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0034', '7de1ffb0-4d7e-4f05-aab5-c99dbd93edf3', 180000, '2026-09-01 11:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer10@okpunjab',
                   '+919875569635', '\x831f2997feff6b0726688507698163489872b77c72950f1541038ff78b1991fc323d3689d14b'::bytea, 'Punjab National Bank', 'TXN26184000034',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-09-01 11:32:49'::timestamp, '2026-09-01 11:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('7de1ffb0-4d7e-4f05-aab5-c99dbd93edf3', 'CMP-20260905-0034', '\xebd930f4626967611217eb4323c30edafd7e663964bd4d975802c36443fd3d55d40bac78c1d778134e5434ba77'::bytea, '\x0dc561ab5e72eab2e328c747c51b39aa83a1bb1dcaa218c7deff93c59448bace15a808e7cb05eb3c60'::bytea,
                    'victim34@example.gov.in', '408 Cyber Park, Mumbai', '\xf685da7faf3802f834a5bdc7abb4ab30ce9fe6ca5ff0c6c5ed00aa6f76228770b088f28f431fec9ebfa75207877bfd28cd9958dba5d5b83659af75'::bytea,
                    'victim34@upi', '2026-09-01 11:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0035', '64b11762-dff2-444d-a966-fb249bd1fae9', 15000, '2026-09-01 07:32:49'::timestamp, 'UPI_FRAUD', 'scammer11@okhdfc',
                   '+919895511909', '\xb6629258c01ccadbdb3463c371ebb61c78056655b0cf50bfc8c5924479bf4623a780d1923158'::bytea, 'HDFC Bank', 'TXN26184000035',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-09-01 07:32:49'::timestamp, '2026-09-01 07:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('64b11762-dff2-444d-a966-fb249bd1fae9', 'CMP-20260905-0035', '\x04694852193130eeef255e2522e08b89c829ddcfe14e7e262ee9a4edc2dd62ab9aa24dfd25b804b24f901bd354'::bytea, '\x99f1e33c3265aecbf1377b544da1708d86eda3e374ebfae88e4190e0fed9f904b26312bdcce72d1480'::bytea,
                    'victim35@example.gov.in', '420 Cyber Park, Mumbai', '\x753efbb35ea249df901ca92c17e314c945e5d19a62548857a27bc66deeee906b0699138c9998291fba22eee05de44b3a'::bytea,
                    'victim35@upi', '2026-09-01 07:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0036', 'ad918e23-b8ca-4cbf-b248-b12bb746b1c9', 45000, '2026-08-28 08:32:49'::timestamp, 'LOAN_APP_FRAUD', 'scammer0@okicici',
                   '+919888183110', '\x5907ea9842be8019938a77444a22bd199ae70d147e8e3e987c368ae09c22824df9c68424fa54'::bytea, 'ICICI Bank', 'TXN26184000036',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-28 08:32:49'::timestamp, '2026-08-28 08:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('ad918e23-b8ca-4cbf-b248-b12bb746b1c9', 'CMP-20260905-0036', '\xdc4afd8aaefc714d2450b82bdf2f1823a4d7765b0bdd08dd9c1b0e33f4d3bace065323e3c6dcc835bdaac896ca'::bytea, '\xe7099c7ff67b3b2b08e5d2ad4071ca7a2684906217a13fb4f6171960e94bda1581775ff470bf62e3dd'::bytea,
                    'victim36@example.gov.in', '432 Cyber Park, Mumbai', '\x7b71a591f9c66ac44677309c26056b40f4f1238f347893006f359d4d9087f2ee4fb5138323009d89dcb5570e0515d6c645'::bytea,
                    'victim36@upi', '2026-08-28 08:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0037', '88284cbb-84e5-411d-8efa-172a27d65e51', 180000, '2026-08-26 05:32:49'::timestamp, 'INVESTMENT_SCAM', 'scammer1@okicici',
                   '+919838195995', '\x42eccacfe93ae1efd118ee4aaaf41e31710c415cc516e39d021895edb4f92c31b949d903f693'::bytea, 'ICICI Bank', 'TXN26184000037',
                   'SUBMITTED'::complaintstatus, user_id, '2026-08-26 05:32:49'::timestamp, '2026-08-26 05:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('88284cbb-84e5-411d-8efa-172a27d65e51', 'CMP-20260905-0037', '\xf54554107600ab59011ab0357d49b1b19e034b6b01b5c22ac8e23d1cc5d8882d755d54fe85ba71b1ff9ebfbb63'::bytea, '\xa37bfdb4aae2f3f564ccc08619f7a3715b152fc9153dbc226592caa0630bfc572375a64683a591a4ef'::bytea,
                    'victim37@example.gov.in', '444 Cyber Park, Mumbai', '\xc580346a2379e78ae8b568de92c8d6a488a791d29b7733707e9e0a499eb58123692cae7f6a49e6e3f0dab3a963ce78c78a'::bytea,
                    'victim37@upi', '2026-08-26 05:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0038', '11ef6358-250c-476f-ae05-7d2ca9dd6cd1', 45000, '2026-09-05 07:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer2@okhdfc',
                   '+919865337219', '\x5570456b1943ddc16e18a523bfc765abed6331da8fe45e7c787630112abd34463934b8c134fb'::bytea, 'HDFC Bank', 'TXN26184000038',
                   'ANALYZING'::complaintstatus, user_id, '2026-09-05 07:32:49'::timestamp, '2026-09-05 07:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('11ef6358-250c-476f-ae05-7d2ca9dd6cd1', 'CMP-20260905-0038', '\x7a33a1c528c4cf909c31381dd60dd65139bc76b6be9347a66af55401dcb1f1684a204fbf83fb8e007231905a01'::bytea, '\xbab78e786b812b08619160cc7eb39ed8a5b4febd84730da4e9718e98bbf479862009ba141c75543078'::bytea,
                    'victim38@example.gov.in', '456 Cyber Park, Mumbai', '\x6b57bb69fde6f10651ebceeba4a299d9970e4032c8f19ad4e8333772c50bc4238fa014ed22ce95ab71cd21dd92b2b75c'::bytea,
                    'victim38@upi', '2026-09-05 07:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0039', 'c4709a7a-801d-4702-a19e-7bd5313d25d1', 28500, '2026-09-01 22:32:49'::timestamp, 'ELECTRICITY_BILL', 'scammer3@okaxis',
                   '+919839854548', '\x4de348c5b052a190e132b2a5a3b4c8a858792e6ca6bf9cdef692673e8880aea8add95b9be872'::bytea, 'Axis Bank', 'TXN26184000039',
                   'SUBMITTED'::complaintstatus, user_id, '2026-09-01 22:32:49'::timestamp, '2026-09-01 22:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('c4709a7a-801d-4702-a19e-7bd5313d25d1', 'CMP-20260905-0039', '\x8ea545768f0c6a3e267796bf0f9fd517bdca9a65e34f5260f3748488bca9ed0d96b0819493266cfc45e2bc01df'::bytea, '\x748e9d48c694da267a2cd01255ac142ce8dc1b7c17b0a305d519c2e88bb601dda809f1fc5c399b3eaa'::bytea,
                    'victim39@example.gov.in', '468 Cyber Park, Mumbai', '\x561870d067880dc85992808418feb2dcc3d5c64747ade0843cb1e2fc5700a1657effdd6f5ead0239f718df60df50baac'::bytea,
                    'victim39@upi', '2026-09-01 22:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0040', 'c1820bdb-190d-43e1-b52c-a4a10143fdc9', 85000, '2026-08-24 04:32:49'::timestamp, 'ELECTRICITY_BILL', 'scammer4@okicici',
                   '+919819317495', '\x431af9ae210cca4e302f154d1ed463b44d410cf56ebac9fdc18615278e15b41f624cde6ca2a5'::bytea, 'ICICI Bank', 'TXN26184000040',
                   'ACTION_TAKEN'::complaintstatus, user_id, '2026-08-24 04:32:49'::timestamp, '2026-08-24 04:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('c1820bdb-190d-43e1-b52c-a4a10143fdc9', 'CMP-20260905-0040', '\x12e8f7b6639e8eb2800e517c1686ffceebd5e88a896a11b41d1fda4c0e79f4c006dd12fb0eadd00ac64edc2286'::bytea, '\xc17aeab92ae398b4baaabf452331735f3ed8b6841a0776d2c110d29fd44e50b97040ac1d600929a383'::bytea,
                    'victim40@example.gov.in', '480 Cyber Park, Mumbai', '\x4af8a9abe3e9f2ff28ef4d4f5d5d19e93128f69ded425aea9ae239d493f7aa597106acf011166de71d24b8b5feb0279003'::bytea,
                    'victim40@upi', '2026-08-24 04:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0041', '091b287c-ebbe-4c55-9350-5df65eee4fa2', 28500, '2026-09-05 09:32:49'::timestamp, 'TASK_SCAM', 'scammer5@okpunjab',
                   '+919845630292', '\x6123b3245bac82b7650bd82c8d57ff6cbcca31c98ce9c5b1c6744640c414d55634b8ce104f47'::bytea, 'Punjab National Bank', 'TXN26184000041',
                   'ANALYZING'::complaintstatus, user_id, '2026-09-05 09:32:49'::timestamp, '2026-09-05 09:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('091b287c-ebbe-4c55-9350-5df65eee4fa2', 'CMP-20260905-0041', '\x15adf47b7703ac373c756f296c641d19969c5081f718e86a9dcc112f18d5c6ea0e3a805759d8e21f7176b15a14'::bytea, '\x57e2d4ee8e686f80742fad8602d589a7cadc6b6d871d5193a4251ba22d2b9feee39fb6f302a916a427'::bytea,
                    'victim41@example.gov.in', '492 Cyber Park, Mumbai', '\xe8b6a25ba13f34ebfaaa623898a2d2be8949b7b6c90801217beb15c79580c0da3f003f4e946b058a378304f2967f58063fa98d574b50d8cac40c8a'::bytea,
                    'victim41@upi', '2026-09-05 09:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0042', '0677a847-01a5-456e-b124-c062fbe3b5e1', 350000, '2026-09-02 04:32:49'::timestamp, 'LOAN_APP_FRAUD', 'scammer6@okaxis',
                   '+919887388337', '\x8cb3295036aa4e262795d6e16a7e7295f2e4f2b8638c3e5c399266c31fa52b240fa045c2c737'::bytea, 'Axis Bank', 'TXN26184000042',
                   'SUBMITTED'::complaintstatus, user_id, '2026-09-02 04:32:49'::timestamp, '2026-09-02 04:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('0677a847-01a5-456e-b124-c062fbe3b5e1', 'CMP-20260905-0042', '\x25c3cbdb61e5f2825a67372366d9d2fc70b98676334fe6ebcbd02b51f5e23feec79e314632eb1354d26823f3ab'::bytea, '\x5ca7853b50aaa92a11f6be2e4ba32768ffed924d0a27917cd933b9d38bc349b5872d66fdd2023dd1b8'::bytea,
                    'victim42@example.gov.in', '504 Cyber Park, Mumbai', '\xfdee1d179afe4d0d1ad70a25e3dc0351a9f3aff28d027a6c3f4b4946949b68ea9825832787b9a73acb0a266161a3307c'::bytea,
                    'victim42@upi', '2026-09-02 04:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0043', 'ccc2d60a-ef6e-4c27-8038-19fc71f09d63', 950000, '2026-09-04 02:32:49'::timestamp, 'INVESTMENT_SCAM', 'scammer7@okicici',
                   '+919867887757', '\xf311ce790bc9f6c59aae0877e0c8617a87c3bbdc2bacbd9ef5313eea298a968ad3ffc55b35d1'::bytea, 'ICICI Bank', 'TXN26184000043',
                   'ANALYZING'::complaintstatus, user_id, '2026-09-04 02:32:49'::timestamp, '2026-09-04 02:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('ccc2d60a-ef6e-4c27-8038-19fc71f09d63', 'CMP-20260905-0043', '\xfd3d137f1d3244338e7ad3d0650e1961d8ec49f7687f9eae4a54204d29a54ef156f6c91c48f0e469bb3d7aaa2a'::bytea, '\xfb6a31b5cfd02e9f2c5ffe2b4d633ec214a35aadd8e8bc896004b386fbbb5c2632a36e91b0c9d548e0'::bytea,
                    'victim43@example.gov.in', '516 Cyber Park, Mumbai', '\x029f1dd0480cd4c04beb4f0702160e559c665e2d601104bd2539b0ba887faea434bc5db47f28f7a2b1dad35695d55a8068'::bytea,
                    'victim43@upi', '2026-09-04 02:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0044', 'fa9139a6-20fa-4f08-bd7f-763be71d8c55', 950000, '2026-08-25 03:32:49'::timestamp, 'TASK_SCAM', 'scammer8@okicici',
                   '+919864009265', '\xe776acbf1980d52b80919eb3012c6d13d3db06d4f0f610335d53960c5a7e04050735a519055f'::bytea, 'ICICI Bank', 'TXN26184000044',
                   'RESOLVED'::complaintstatus, user_id, '2026-08-25 03:32:49'::timestamp, '2026-08-25 03:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('fa9139a6-20fa-4f08-bd7f-763be71d8c55', 'CMP-20260905-0044', '\xcb11eca3c468b98e1b22aee5cde2606afb767c8452576a992bee979cb7d268afe553f9809c583cdea60e97e7b6'::bytea, '\xb05094a42d489e44b72a1e09c71cf436be04fb4152b828f21fa6532534d1e1680d6cab4a440c644ea7'::bytea,
                    'victim44@example.gov.in', '528 Cyber Park, Mumbai', '\x09387b703ae7e86415588337f89a6c47219e63632cc59d414c96ba3514b68c834a95843795ab559142fe694df68973860d'::bytea,
                    'victim44@upi', '2026-08-25 03:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0045', '570ed5c1-b5f5-48f1-b2fe-d1c0963917ae', 350000, '2026-09-01 00:32:49'::timestamp, 'PHISHING', 'scammer9@okpunjab',
                   '+919886384014', '\x9fecd96a60f0863b9660d0047fd1976ac35d8130334105c9538192e3390123e615dcaa03123f'::bytea, 'Punjab National Bank', 'TXN26184000045',
                   'ANALYZING'::complaintstatus, user_id, '2026-09-01 00:32:49'::timestamp, '2026-09-01 00:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('570ed5c1-b5f5-48f1-b2fe-d1c0963917ae', 'CMP-20260905-0045', '\x068b3d98d97ac63895736165a85876d882887b59afd9c0daca0a51963d2c0af8c1dc7b9480c94df4e20cbd8377'::bytea, '\xebd2da93a75c2e1394bdf1c9a0f9050eeb87a19973ce1f7ba59cf2742815961e65fbf521f991571639'::bytea,
                    'victim45@example.gov.in', '540 Cyber Park, Mumbai', '\x1aa8c66d73dec85c6c5a2d6184a4e8f397068f0e690f28f067fe7270569812236b20bf57b1b12d89bb3a6ad135d08e8de4f6ce7cba1040f6391ce7'::bytea,
                    'victim45@upi', '2026-09-01 00:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0046', '800083af-654d-40fd-a82e-31763806de68', 120000, '2026-08-26 02:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer10@okpunjab',
                   '+919891424737', '\x5170c4331262ddd545f17acc8a3c67bbab6fa6bdc4c9aff59a0cd6184d3c2a2667a0b918c59b'::bytea, 'Punjab National Bank', 'TXN26184000046',
                   'RESOLVED'::complaintstatus, user_id, '2026-08-26 02:32:49'::timestamp, '2026-08-26 02:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('800083af-654d-40fd-a82e-31763806de68', 'CMP-20260905-0046', '\x7d21d856bfc96cdcf051b350f11eed625664e6088d8b8f12997abaee58f02de5f152d1dbe1113dc5540224ccad'::bytea, '\x621171b9a6ab2262155f28b05cc31436683c0098bcf6cbdafc8bc141f0e626022267c1150483b6ece6'::bytea,
                    'victim46@example.gov.in', '552 Cyber Park, Mumbai', '\xcdb13add3978f004ea21150cfc59fddec282da58f8369e30eab43a99f20413e5678d50926f84ad0f4448fdde13c68ed649fd13a6b8769b130c4c7e'::bytea,
                    'victim46@upi', '2026-08-26 02:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0047', '5d9eb0c4-e369-49d8-b7d6-005ccd63b1ee', 950000, '2026-08-31 20:32:49'::timestamp, 'ELECTRICITY_BILL', 'scammer11@okkotak',
                   '+919821381064', '\xa2e882cff9e4c1b91943f4e99cd113ec1af3bb0462f3bd318eddc8eeb33ea2f4ab8a55848242'::bytea, 'Kotak Mahindra Bank', 'TXN26184000047',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-31 20:32:49'::timestamp, '2026-08-31 20:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('5d9eb0c4-e369-49d8-b7d6-005ccd63b1ee', 'CMP-20260905-0047', '\x97f6e7e88ff7df21b411d0886a676243a8314a6b595fd7385331dfecffcf6bb38964faeabc31b737fea5037579'::bytea, '\xfbe3d58ca864be3e68298524153a928793e48f9db277be3fdd52a931792e1a3f6cf182524a35a5a65c'::bytea,
                    'victim47@example.gov.in', '564 Cyber Park, Mumbai', '\x81deff087c5eab238ef62959260c1693d0d45a2b07b2ba910b5dd57ef6c9e390ac4c5715f18ef98d36cb53aee339211af7da6b32fad69915089e'::bytea,
                    'victim47@upi', '2026-08-31 20:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0048', '3f5435e0-14f7-4800-ad51-ea35f6360081', 120000, '2026-09-05 05:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer0@okhdfc',
                   '+919813278320', '\x3b680b88c2bc8d3023aae22c502c78501faa6ceb0503f42e25d438dbebe7a3b44b2c57b8cdbc'::bytea, 'HDFC Bank', 'TXN26184000048',
                   'ANALYZING'::complaintstatus, user_id, '2026-09-05 05:32:49'::timestamp, '2026-09-05 05:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('3f5435e0-14f7-4800-ad51-ea35f6360081', 'CMP-20260905-0048', '\x67303b333317cbd6759e8ca76fca4022028b89c1f21ecc841122b766ffd5e73341bfa70035607e0cf8f0f21f7d'::bytea, '\xea677fa34738941a7581ff627ce44dd7410c0ad8b5a3a1924b1eb91e111ffcfe564e0be37cdb5f1dfe'::bytea,
                    'victim48@example.gov.in', '576 Cyber Park, Mumbai', '\xa4d74e38788c647d458ce4796081c3688e4ef470a3a8f21afd8b4e73a145f59d40abd04217e4fe631f64c0c2e600ccb9'::bytea,
                    'victim48@upi', '2026-09-05 05:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0049', 'ff8a0b98-dcb1-4735-99c2-51a5ef6a15ad', 350000, '2026-08-29 00:32:49'::timestamp, 'PHISHING', 'scammer1@okkotak',
                   '+919861536717', '\x3e384682e956548348f19c44b6925cd2949f1fbdbccb690abb7744a54ff0ae8e452f4719fd46'::bytea, 'Kotak Mahindra Bank', 'TXN26184000049',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-29 00:32:49'::timestamp, '2026-08-29 00:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('ff8a0b98-dcb1-4735-99c2-51a5ef6a15ad', 'CMP-20260905-0049', '\x2808f67a5a3d82e5090c9274f37e6e4e8bc758f32436374553a0c670060bc7d336e6b11f820f318764f7cb3043'::bytea, '\xa4c88a44ad09ed5adc455065de2b3352475592c3fb2d37f420c680a9760b8d28a756d9680ad315e714'::bytea,
                    'victim49@example.gov.in', '588 Cyber Park, Mumbai', '\x8c3a18b0a68b2ee69fe7ed517d0eb8e4a86da0882092bc73b5d61eecdb37374b246172cf5e7dae165c6eb90f52fedcbd51c946cef0827cdc7ef5'::bytea,
                    'victim49@upi', '2026-08-29 00:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT 'CMP-20260905-0050', 'e8c60fba-399a-47f4-b659-fd8c48ba0405', 350000, '2026-08-29 11:32:49'::timestamp, 'DIGITAL_ARREST', 'scammer2@okkotak',
                   '+919879519112', '\xdb65b6cd1d6ae9e1fe9055e90fb1b0ab15245a6f2bcbc61578476df4df9c1578793f85fa380e'::bytea, 'Kotak Mahindra Bank', 'TXN26184000050',
                   'ANALYZING'::complaintstatus, user_id, '2026-08-29 11:32:49'::timestamp, '2026-08-29 11:32:49'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        

            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('e8c60fba-399a-47f4-b659-fd8c48ba0405', 'CMP-20260905-0050', '\x77d2fa82b2dcc021cab15e4f952781f14acfabfd6684c298e2073c6fc08555fc4643ac6a57e4431bc667b58bee'::bytea, '\xe17fce1044d362f6b6943049f869149242bd63013c1b0c713d6e04a6282d50be34fc8a0db82aa39932'::bytea,
                    'victim50@example.gov.in', '600 Cyber Park, Mumbai', '\xdacb1cfceed1c21256ebb5763a79207b06fd53f8f3cdd4dd5acb90c4d1466e152ef39267dee498a068d86bd0f660d5ea2c020e35cb11f1eb652d'::bytea,
                    'victim50@upi', '2026-08-29 11:32:49'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'b924c50b-6b03-4547-ab14-fc1dd2d90896', 'CMP-20260905-0009', 'whatsapp_chat_evidence.png', 'image/png', 'ef44911601d44530bd7878b055fdce39', 'bafyf41e962d677d4adca5a6602d', now() - interval '1 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '599d3e98-03ee-4b5b-b424-1dcce0da66ac', 'CMP-20260905-0043', 'imps_transaction_slip.pdf', 'application/pdf', '46647b39b5574893a466ea4da30577d1', 'bafy251a486a6e004e0fa42259a0', now() - interval '2 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '1d775b62-0e97-44f6-b5ca-4abfdb3f2313', 'CMP-20260905-0036', 'imps_transaction_slip.pdf', 'application/pdf', 'dd5bfa657c8f4d47a753b2e612abee8b', 'bafy53e0c9cd675547df915e1722', now() - interval '3 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '50a2c196-9b84-4dd5-af26-4a283df2f431', 'CMP-20260905-0021', 'whatsapp_chat_evidence.png', 'image/png', '6429a17e6a4646759165dad7f68dc4c9', 'bafy4b76436d27e648cf90bc2af8', now() - interval '4 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'f70d381a-cd7b-43ac-9966-eb37410aa775', 'CMP-20260905-0040', 'mule_network_topology.json', 'application/json', '284dffde62c0421a819aa102aab5ea96', 'bafye4ca116349a74c25a240e93c', now() - interval '5 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '44caf860-dc6b-4a34-af4e-22707b965cf6', 'CMP-20260905-0033', 'whatsapp_chat_evidence.png', 'image/png', 'aeb85751feef44cba81334ad85b20c53', 'bafy14ee66dd2c9b41669c593799', now() - interval '6 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'f5bcb382-7ae7-43e1-b439-16e354f88bb6', 'CMP-20260905-0036', 'whatsapp_chat_evidence.png', 'image/png', '32e37faf46ec49c1bb7193fb4b89485d', 'bafy64dab56d301e46a9a33f2e8c', now() - interval '7 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '4d5834cf-b3a0-4d09-9cd9-426c89efd191', 'CMP-20260905-0011', 'mule_network_topology.json', 'application/json', 'fcdd8d8cbb5147ee9db83cb7463cf100', 'bafy4fa6ca7166ee40a6987d5a22', now() - interval '8 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '54b6422f-90fc-4ac5-82ce-b4aee1702754', 'CMP-20260905-0031', 'whatsapp_chat_evidence.png', 'image/png', '581c8cab917346be9954d23c8670cf86', 'bafya1a7243bb380457f96745aad', now() - interval '9 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'c5fa3012-ed4a-4faa-af40-32a90938bba5', 'CMP-20260905-0017', 'bank_statement_axis.pdf', 'application/pdf', '3be81705543d4c6a813669994f738585', 'bafy4bac063330544785923e2327', now() - interval '10 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '6f3682ff-df51-439c-b04f-8eb1c478cc31', 'CMP-20260905-0041', 'digital_arrest_evidence.pdf', 'application/pdf', '15aa9cb6734a4f40b50bfcc6ddbe408b', 'bafy18c1d4e0e53444e1b54fd613', now() - interval '11 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'a14b5c76-fb40-4515-9d6b-9eea2fd0ac4b', 'CMP-20260905-0050', 'imps_transaction_slip.pdf', 'application/pdf', '3ce8a5c1784a4d04968d2579aa3c4b68', 'bafyc0934e0039724b74b41fe3b4', now() - interval '12 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '0792937f-19ac-44e6-b89e-5aced2554dd1', 'CMP-20260905-0032', 'mule_network_topology.json', 'application/json', '632846a5d1af46f0a324f9a8d8f6e7c2', 'bafye71cd0d2725e44779d2955d5', now() - interval '13 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '2b378d99-9042-477e-bc9a-08ba93098d74', 'CMP-20260905-0016', 'digital_arrest_evidence.pdf', 'application/pdf', 'baab9610a6e24668a5e21afbc9ef1815', 'bafy7d70bb1116a64a309ecdf2f1', now() - interval '14 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '7b4d82a9-444f-49a5-b1e4-6ca010443f48', 'CMP-20260905-0029', 'fir_sample_test.pdf', 'application/pdf', 'b94c4c8e22144493b5b5b1a7eda48115', 'bafy727187b01d9043f2b64d23bd', now() - interval '15 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '98adcd6f-2087-4d3d-8e50-d3124007b762', 'CMP-20260905-0046', 'digital_arrest_evidence.pdf', 'application/pdf', '7bee805247dd494299fcd81c8d4ca487', 'bafy1a938b5205d24553824ac725', now() - interval '16 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '5470b49a-7414-47de-ad74-13d9c9e5e3d5', 'CMP-20260905-0016', 'digital_arrest_evidence.pdf', 'application/pdf', 'df0a04d3856f47ec998f3101e477e2fd', 'bafy15f2010a41804126a960a91b', now() - interval '17 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'b571d20f-9ac2-4e05-85e0-4ad00102d12f', 'CMP-20260905-0022', 'digital_arrest_evidence.pdf', 'application/pdf', '1bc13b91cc1d445bb81c5e161613ee3d', 'bafy831a066e667649a0a974b0d2', now() - interval '18 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'da126a30-e34b-49e5-a4bb-2ab64c208c70', 'CMP-20260905-0035', 'fir_sample_test.pdf', 'application/pdf', '97fdb24e1dc143dcaa529698fc788860', 'bafy3e49fb57a2e64e169d70db9c', now() - interval '19 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'e417f321-b1b5-4e69-bb9b-856a97694326', 'CMP-20260905-0009', 'bank_statement_axis.pdf', 'application/pdf', '210cc1c6cab74ff38eac3935aad51495', 'bafya211f231c2524fd180ba23f4', now() - interval '20 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '3a839cc7-e99f-4cce-a8aa-e1057c99260a', 'CMP-20260905-0015', 'whatsapp_chat_evidence.png', 'image/png', '69d91cf0f3a9498f9fa69f15a61346c6', 'bafy16d9472e6e6d4321aae66f56', now() - interval '21 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'f12fddbb-b9c4-4a90-8053-cd19dc84fd76', 'CMP-20260905-0045', 'bank_statement_axis.pdf', 'application/pdf', '6d354f2302464169b84faea78d213526', 'bafy32798017bc3b42e4812ea9ba', now() - interval '22 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'ffc036a8-8d1f-4d0a-9700-8c3a32538815', 'CMP-20260905-0046', 'bank_statement_axis.pdf', 'application/pdf', '4e357a2342754bfe8875558396a974f4', 'bafy6e5a6fb25580490f84fe1a8f', now() - interval '23 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT 'b7f6f2e8-7395-4e30-b811-bb7163cf547c', 'CMP-20260905-0005', 'whatsapp_chat_evidence.png', 'image/png', 'f8e686fef4f54669a816f181e27df55e', 'bafy8f0ea367d1004b6d8609cb72', now() - interval '24 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '8c2cd39e-29cb-4ed5-8e55-fadc20e74caf', 'CMP-20260905-0027', 'digital_arrest_evidence.pdf', 'application/pdf', '5a175d3b1a904c5fac8c2d7b9d844223', 'bafy8616c83f0e764cbfb666591f', now() - interval '25 hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '0531a3f0-696d-41a8-aca1-5612ec4c7bdc', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0030", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '1 hours', '10.40.1.2'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '14fbbea1-9e74-4bed-9cac-c358806b4f82', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0004", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '2 hours', '10.40.2.3'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '06cb580e-50fe-4347-b57a-89a35ce96466', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0027", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '3 hours', '10.40.3.4'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '13f5526a-92c4-4c7a-8ce1-99edc0b84d38', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0050", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '4 hours', '10.40.4.5'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '420eb1bd-42a8-426b-868f-be65fa299a25', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0045", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '5 hours', '10.40.5.6'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '1ae74a03-72af-447b-891b-8396264b8942', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0049", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '6 hours', '10.40.6.7'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '66295dd0-6d14-451f-80c9-dd96de34dff5', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0025", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '7 hours', '10.40.7.8'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '1b7cbe59-0397-40f3-b60c-723a75c83e7d', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0001", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '8 hours', '10.40.8.9'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '290f5ad1-6828-4bcf-8c2f-ec2191f55171', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0020", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '9 hours', '10.40.9.10'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '5b0196ed-805c-4a9f-8894-b5f4dc00a908', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0025", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '10 hours', '10.40.0.11'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '42035090-cff9-4e93-8c7c-7fd66525dfcd', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0027", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '11 hours', '10.40.1.12'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '35b254b7-07f5-47cb-baf8-17a49023fe32', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0048", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '12 hours', '10.40.2.13'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '57ab0214-c17c-4b2f-ae9c-bc27f4002397', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0035", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '13 hours', '10.40.3.14'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '2feb0ddf-f0dc-4b1a-b3c3-443e94c19133', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0039", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '14 hours', '10.40.4.15'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'dd94c4ae-3967-49e5-89d5-826104686d45', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0032", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '15 hours', '10.40.5.16'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '47531673-fa0f-48a6-8a17-3d9efd018f1b', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0018", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '16 hours', '10.40.6.17'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '2718e0ae-ffdd-4e5f-b7b2-5a029c0f87eb', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0032", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '17 hours', '10.40.7.18'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'd8e89bf4-b59e-42d9-9a99-fc150dd7bda2', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0025", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '18 hours', '10.40.8.19'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'cde598da-34cc-4faa-803b-229dd13fdeec', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0043", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '19 hours', '10.40.9.20'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '939af96b-5926-4831-afc6-f62a1f1e084c', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0026", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '20 hours', '10.40.0.21'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '17ac2dea-1555-467c-921a-3410b883fd65', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0011", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '21 hours', '10.40.1.22'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '5c1df352-8b3d-4995-a8fc-038a2bce9068', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0030", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '22 hours', '10.40.2.23'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'db61d067-7100-4dc2-930e-e4d5b6f96fbd', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0040", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '23 hours', '10.40.3.24'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '50c511df-50a2-4f7f-b19c-8a6593d700a7', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0002", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '24 hours', '10.40.4.25'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '973f919d-db40-4fb4-95cc-9489786c3def', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0038", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '25 hours', '10.40.5.26'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '1335db5f-1b83-4b76-9e00-622f770cb35b', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0043", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '26 hours', '10.40.6.27'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '2fd763ad-faf3-4758-9a5b-f2578a345752', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0006", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '27 hours', '10.40.7.28'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'a436873a-e178-4339-8ed9-82de828fd678', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0028", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '28 hours', '10.40.8.29'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '9737a5d9-042b-474f-9ddb-9f2d49cc49ec', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0030", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '29 hours', '10.40.9.30'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '0799921d-2416-4967-8a87-76c8a97ab6d6', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0004", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '30 hours', '10.40.0.31'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '853b3aaf-b267-4366-9b5d-8c7def22b74c', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0025", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '31 hours', '10.40.1.32'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '32071873-c526-4711-a0b5-3ad2f3e41777', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0014", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '32 hours', '10.40.2.33'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '939a6daa-af0b-40c2-a45f-d4893c1c837d', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0021", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '33 hours', '10.40.3.34'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '93112357-d1c5-4874-8c35-bfdcd2a2b94f', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0049", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '34 hours', '10.40.4.35'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'f21b12b3-3a4a-4906-8624-68f0cd4f17f3', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0018", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '35 hours', '10.40.5.36'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'fe7b335f-4cd7-4886-baaa-0ec4fe35d440', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0027", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '36 hours', '10.40.6.37'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '8ac997b9-c2b2-44b7-a707-caae53fdf426', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0006", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '37 hours', '10.40.7.38'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '5551f039-98f1-453d-996d-1f6063cd28e3', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0002", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '38 hours', '10.40.8.39'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '45f0bf0f-79a1-4e6e-ba43-6cd89944e4b9', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0035", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '39 hours', '10.40.9.40'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'edc54e91-1c7e-4729-96c9-f00aa8b1823a', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0023", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '40 hours', '10.40.0.41'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'd8ec0e2d-0e3e-425a-84ea-8242fdd48a06', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0042", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '41 hours', '10.40.1.42'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '3aab9de4-b9ae-489c-a154-9e907144401a', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0050", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '42 hours', '10.40.2.43'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '91d9fabb-543f-4777-8060-0aa0c077ca19', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0003", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '43 hours', '10.40.3.44'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '9b070ec0-923c-4a9a-81ac-287f1c3900cd', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0002", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '44 hours', '10.40.4.45'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'de0c2b82-f1f5-43af-897e-1da9e88fd4b6', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0013", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '45 hours', '10.40.5.46'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '755bb6cf-7ef5-4cd2-a53d-8dc1fb5adafa', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0002", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '46 hours', '10.40.6.47'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'c7601bef-e09f-4c7c-b4fa-fcab4afd6541', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0010", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '47 hours', '10.40.7.48'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '6c5afa67-e6d0-4284-9ebb-e2a7c5d5bba6', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0009", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '48 hours', '10.40.8.49'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '6cda90a0-eda6-4c6b-9a44-4639a82f7f28', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0043", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '49 hours', '10.40.9.50'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'b8060d9c-683f-46c3-a113-6cbd953cd99b', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0037", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '50 hours', '10.40.0.51'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'ed27d20a-b7bd-4ebc-8567-01f8d9fb4856', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0030", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '51 hours', '10.40.1.52'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '075a22b0-ae5a-4d98-90f2-504a2b455cdc', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0017", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '52 hours', '10.40.2.53'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '39948851-12b9-4539-be79-0a256188f453', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0024", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '53 hours', '10.40.3.54'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '5046a0a6-26e0-46dd-8e2f-8691e1fcdbd5', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0039", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '54 hours', '10.40.4.55'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '909bd3f5-7c99-4035-be2a-bf7e52db9a69', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0048", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '55 hours', '10.40.5.56'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'e63fd33c-af37-4df3-8168-6488a95d182f', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0008", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '56 hours', '10.40.6.57'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '5b417534-ceb1-436b-ad43-176ee92bb783', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0011", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '57 hours', '10.40.7.58'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '1f8ffdb9-0501-452e-8eaa-89358b7c8fc3', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0007", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '58 hours', '10.40.8.59'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '2ee55ce3-4a36-44b9-9f84-4cdb7cf82eaa', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0002", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '59 hours', '10.40.9.60'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '22152ee0-22dd-4fb0-a1f9-7342e9cd53f0', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0037", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '60 hours', '10.40.0.61'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '51f267d6-efe0-4dde-b751-d8e6002fe000', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0025", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '61 hours', '10.40.1.62'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'b6b906ee-1345-46b0-9e46-27c13bdfe25b', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0046", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '62 hours', '10.40.2.63'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'ee373159-a8e8-4d50-856e-3422b7b7def1', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0005", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '63 hours', '10.40.3.64'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'a4b4d28a-8ff7-46a0-86a1-6c7f1440ad65', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0045", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '64 hours', '10.40.4.65'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'b0673dc2-e58f-4a1c-abab-dec55f7bdaa6', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0041", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '65 hours', '10.40.5.66'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'ad2d53c7-319a-49c4-be3f-a043b4b7dc63', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0007", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '66 hours', '10.40.6.67'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '2dac529f-9ce9-4d23-a33e-1a463ba4bde1', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0050", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '67 hours', '10.40.7.68'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'b45e9215-2d05-43d5-926c-5aeb423b6916', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0044", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '68 hours', '10.40.8.69'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '32bb8519-0261-44e4-84ec-6798a98234ce', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0008", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '69 hours', '10.40.9.70'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'e6adca76-068c-4fea-ab82-821c2fb7f390', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0037", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '70 hours', '10.40.0.71'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'b02439f4-9b1b-4279-a5b3-dffd6f6c2bab', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0003", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '71 hours', '10.40.1.72'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '0a54bd53-395b-4010-b7e2-3bb98b6d44db', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0035", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '72 hours', '10.40.2.73'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '0852f3e3-5d2d-4474-8726-0c1e054985db', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0043", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '73 hours', '10.40.3.74'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'a854efb4-3ae4-4658-afd1-9d9eee1d73db', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0005", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '74 hours', '10.40.4.75'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '3e73ffd1-8cac-4f84-89e7-9fcd931c60bc', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0042", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '75 hours', '10.40.5.76'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'fefdb9ab-08b3-47dc-b25b-08de51eae732', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0001", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '76 hours', '10.40.6.77'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'e9d1b5a5-ae78-4344-a29f-3b8f8e1012e1', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0027", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '77 hours', '10.40.7.78'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '281a4a0a-80f2-41a5-a39b-fdd97d12fcfb', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0032", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '78 hours', '10.40.8.79'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '3f9115a2-7e54-4247-a334-f6efe215bc60', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0028", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '79 hours', '10.40.9.80'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'e61464de-f332-4a9a-ac38-66d078be3563', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0041", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '80 hours', '10.40.0.81'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'ced5f75e-9f43-4eb7-a18b-aef15d373470', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0030", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '81 hours', '10.40.1.82'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'c8166737-9517-42db-86f0-0683f83447f8', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0010", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '82 hours', '10.40.2.83'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'a6a0b7ce-326d-41e8-ac75-4e46ea92dcc9', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0012", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '83 hours', '10.40.3.84'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '04349819-7104-4673-ba2e-591f544de1fc', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0034", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '84 hours', '10.40.4.85'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '175a0d8a-eba6-460f-9b02-88d463670c9e', user_id, 'ATM_DISPATCH_TRIGGERED', '{"complaint_id": "CMP-20260905-0018", "action": "ATM_DISPATCH_TRIGGERED", "severity": "INFO"}'::jsonb, now() - interval '85 hours', '10.40.5.86'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'd08466ab-1e6c-4160-bcd8-3018f53ef5df', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0035", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '86 hours', '10.40.6.87'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '52ba6e42-ed58-439b-b044-6bbbdc599d99', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0031", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '87 hours', '10.40.7.88'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '85fa8ddc-aa5a-4d23-9c2f-0b9c400bcd62', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0028", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '88 hours', '10.40.8.89'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'fc01b00d-a2b4-4f0d-a903-e66643838839', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0047", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '89 hours', '10.40.9.90'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'f70692cd-b1ab-4d2b-bd9e-332597373ab5', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0018", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '90 hours', '10.40.0.91'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'de4823e5-2dd4-44a0-ba85-dbf435a4cdf9', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0016", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '91 hours', '10.40.1.92'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'a1e8866c-a11d-4b64-8e93-717b3eaa4c84', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0006", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '92 hours', '10.40.2.93'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'b1b76391-8b51-4f09-b7ab-4543ffcbbac7', user_id, 'EVIDENCE_UPLOADED', '{"complaint_id": "CMP-20260905-0029", "action": "EVIDENCE_UPLOADED", "severity": "INFO"}'::jsonb, now() - interval '93 hours', '10.40.3.94'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '32723e6d-9fce-4d7b-bd9f-c11b63ef794e', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0049", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '94 hours', '10.40.4.95'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '98c1af0d-37ae-4544-bcc1-44e644656665', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0037", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '95 hours', '10.40.5.96'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '47d22ddd-7772-4974-9766-034e459b84b5', user_id, 'BANK_FREEZE_NOTICE_ISSUED', '{"complaint_id": "CMP-20260905-0043", "action": "BANK_FREEZE_NOTICE_ISSUED", "severity": "HIGH"}'::jsonb, now() - interval '96 hours', '10.40.6.97'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '0badf17a-e748-44a7-89ac-6754b9f1c4ac', user_id, 'MULE_SUSPECT_IDENTIFIED', '{"complaint_id": "CMP-20260905-0022", "action": "MULE_SUSPECT_IDENTIFIED", "severity": "INFO"}'::jsonb, now() - interval '97 hours', '10.40.7.98'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '3e8a6cea-9305-435a-a2fe-e7357f60b329', user_id, 'COMPLAINT_CREATED', '{"complaint_id": "CMP-20260905-0032", "action": "COMPLAINT_CREATED", "severity": "INFO"}'::jsonb, now() - interval '98 hours', '10.40.8.99'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'adff7f1f-6fd9-4aac-a638-b44a3cefbf5e', user_id, 'CASE_RESOLVED', '{"complaint_id": "CMP-20260905-0021", "action": "CASE_RESOLVED", "severity": "INFO"}'::jsonb, now() - interval '99 hours', '10.40.9.100'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT 'c72d8961-90e4-446b-9dfa-64431ff77d72', user_id, 'STATUS_UPDATED', '{"complaint_id": "CMP-20260905-0032", "action": "STATUS_UPDATED", "severity": "INFO"}'::jsonb, now() - interval '100 hours', '10.40.0.101'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('6cb8d915-2477-4046-ad44-9d11ac54c2f1', 'MULE_ACC_1001', 'CMP-20260905-0014', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '2 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('077fcfab-8a55-4d5a-9a89-5bea97a86b6c', 'MULE_ACC_1002', 'CMP-20260905-0017', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '4 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('8e092014-34c2-4921-9396-ad8f968b608d', 'MULE_ACC_1003', 'CMP-20260905-0018', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '6 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('e67d649f-0b70-4b1d-8ec9-d6150357c050', 'MULE_ACC_1004', 'CMP-20260905-0036', 0.88, 0.92, 0.9, 'HIGH', now() - interval '8 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('c7856b25-af50-45a7-9260-8ddc8dc86316', 'MULE_ACC_1005', 'CMP-20260905-0034', 0.94, 0.85, 0.91, 'HIGH', now() - interval '10 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('2819dfd0-88ed-4826-8906-610e42e8f58c', 'MULE_ACC_1006', 'CMP-20260905-0006', 0.94, 0.85, 0.91, 'HIGH', now() - interval '12 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('58369c56-f94a-45e5-b0c3-dc4ea0099712', 'MULE_ACC_1007', 'CMP-20260905-0047', 0.15, 0.2, 0.17, 'LOW', now() - interval '14 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('08d5227e-a766-4e49-b1f1-a5857d12879d', 'MULE_ACC_1008', 'CMP-20260905-0032', 0.94, 0.85, 0.91, 'HIGH', now() - interval '16 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('c68f2bae-fdcb-43f7-a9b0-49c3b56d9ac6', 'MULE_ACC_1009', 'CMP-20260905-0045', 0.15, 0.2, 0.17, 'LOW', now() - interval '18 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('4f861e92-4a24-474c-b0d5-30082262432e', 'MULE_ACC_1010', 'CMP-20260905-0042', 0.15, 0.2, 0.17, 'LOW', now() - interval '20 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('d5adb28f-fdd8-4a70-9738-10e01a45a881', 'MULE_ACC_1011', 'CMP-20260905-0029', 0.88, 0.92, 0.9, 'HIGH', now() - interval '22 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('c3bd78ac-7198-4bd8-97ad-f16869b4a3b8', 'MULE_ACC_1012', 'CMP-20260905-0006', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '24 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('866acca7-980e-4273-bf8e-e5f45f5bd802', 'MULE_ACC_1013', 'CMP-20260905-0015', 0.15, 0.2, 0.17, 'LOW', now() - interval '26 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('69415f66-d32c-4c3f-9fb6-85851767fd80', 'MULE_ACC_1014', 'CMP-20260905-0045', 0.94, 0.85, 0.91, 'HIGH', now() - interval '28 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('6510a102-e831-419a-b7ae-b9d3aac117d8', 'MULE_ACC_1015', 'CMP-20260905-0020', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '30 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('5de3460a-c603-439e-bfea-792d537a58a4', 'MULE_ACC_1016', 'CMP-20260905-0031', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '32 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('4e72cffc-d7e3-4817-b972-37f90819def8', 'MULE_ACC_1017', 'CMP-20260905-0028', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '34 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('7278e693-4847-451d-8249-2ed8d3281e87', 'MULE_ACC_1018', 'CMP-20260905-0023', 0.15, 0.2, 0.17, 'LOW', now() - interval '36 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('4d2a4190-37ed-4409-9f8c-df810403990e', 'MULE_ACC_1019', 'CMP-20260905-0018', 0.65, 0.7, 0.67, 'MEDIUM', now() - interval '38 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('943c24fb-0660-4d3e-a2a1-a68cd26387e6', 'MULE_ACC_1020', 'CMP-20260905-0017', 0.94, 0.85, 0.91, 'HIGH', now() - interval '40 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('f238af2d-dfc7-41a2-843d-007a498b620a', 'MULE_ACC_1021', 'CMP-20260905-0008', 0.94, 0.85, 0.91, 'HIGH', now() - interval '42 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('a956703d-962c-497b-b86d-a2e540cced5f', 'MULE_ACC_1022', 'CMP-20260905-0021', 0.88, 0.92, 0.9, 'HIGH', now() - interval '44 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('c1e7ada2-9e56-4cab-9a29-c912ea3ac473', 'MULE_ACC_1023', 'CMP-20260905-0048', 0.94, 0.85, 0.91, 'HIGH', now() - interval '46 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('d1ff9f78-db3f-452d-9f81-a82b2ff6847a', 'MULE_ACC_1024', 'CMP-20260905-0013', 0.94, 0.85, 0.91, 'HIGH', now() - interval '48 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('cc535970-a870-42c6-aa21-b8e599254890', 'MULE_ACC_1025', 'CMP-20260905-0048', 0.15, 0.2, 0.17, 'LOW', now() - interval '50 hours')
            ON CONFLICT (score_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('1471eebf-e0e2-45a3-bb95-3cd9bea18b6a', 'CMP-20260905-0018', 'ATM_DEL_CP_05', 0.954, 2.8, now() - interval '3 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('03c079e0-97a6-497f-8d71-554ffca3d4cb', 'CMP-20260905-0019', 'ATM_MUM_ANDHERI_02', 0.92, 2.2, now() - interval '6 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('ee5bdc0e-64c3-4ccf-8de8-aa1665ed064a', 'CMP-20260905-0024', 'ATM_MUM_ANDHERI_03', 0.793, 3.3, now() - interval '9 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('9da5d0b2-59b8-489d-8d10-62eb00938478', 'CMP-20260905-0009', 'ATM_MUM_ANDHERI_05', 0.731, 1.6, now() - interval '12 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('a2973377-5f70-455e-992d-0003acbbd962', 'CMP-20260905-0019', 'ATM_MUM_ANDHERI_03', 0.873, 3.4, now() - interval '15 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('a9409b13-fee9-4519-9e69-f381e382695e', 'CMP-20260905-0007', 'ATM_MUM_ANDHERI_01', 0.858, 2.7, now() - interval '18 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('1bdd24bf-ee83-40d4-8342-97e8f54a522a', 'CMP-20260905-0029', 'ATM_DEL_CP_01', 0.764, 1.6, now() - interval '21 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('3e48a86f-24c3-4899-a91e-08b5b7f614bc', 'CMP-20260905-0031', 'ATM_MUM_ANDHERI_02', 0.917, 2.5, now() - interval '24 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('10ec415b-df7c-4e6c-b741-82d8fd3907bd', 'CMP-20260905-0005', 'ATM_DEL_CP_05', 0.871, 1.6, now() - interval '27 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('5c1f58fc-d489-4a83-8f7d-36b7a9a56e39', 'CMP-20260905-0010', 'ATM_DEL_CP_05', 0.948, 1.7, now() - interval '30 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('505d8c8b-a5d0-45f8-9eae-03d21d0e239f', 'CMP-20260905-0016', 'ATM_MUM_ANDHERI_02', 0.854, 2.5, now() - interval '33 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('bc4e4c33-53a4-4a24-91bb-ab9862ff51d3', 'CMP-20260905-0039', 'ATM_DEL_CP_05', 0.774, 2.8, now() - interval '36 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('6743725b-556f-4a1e-b7c6-08335b3be42e', 'CMP-20260905-0029', 'ATM_DEL_CP_03', 0.791, 3.0, now() - interval '39 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('9eeae9c3-92a9-4289-90b9-79193f57fe90', 'CMP-20260905-0028', 'ATM_MUM_ANDHERI_05', 0.856, 1.7, now() - interval '42 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('edeb50a0-c3e7-4574-a935-60b04f21c6cb', 'CMP-20260905-0048', 'ATM_MUM_ANDHERI_02', 0.947, 2.0, now() - interval '45 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('b77ef905-aa85-4811-b5fd-193e50459c17', 'CMP-20260905-0014', 'ATM_MUM_ANDHERI_05', 0.879, 1.9, now() - interval '48 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('563ed1d5-f975-4422-a4e2-2cff2ec07b7d', 'CMP-20260905-0012', 'ATM_DEL_CP_04', 0.738, 1.5, now() - interval '51 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('9a650619-40a4-42af-b96f-a745afff3426', 'CMP-20260905-0029', 'ATM_DEL_CP_05', 0.833, 1.6, now() - interval '54 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('8fc381ea-3e25-45cb-a2a3-3bb91b83e42e', 'CMP-20260905-0019', 'ATM_MUM_ANDHERI_05', 0.889, 2.6, now() - interval '57 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('222bb79e-540d-4e23-b02b-42779e82c0bc', 'CMP-20260905-0044', 'ATM_MUM_ANDHERI_04', 0.942, 3.5, now() - interval '60 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('a324b16c-5088-4105-8825-24b2cc4284d8', 'CMP-20260905-0041', 'ATM_DEL_CP_05', 0.879, 3.8, now() - interval '63 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('c566d8f1-3d2b-401a-bd18-3e927a6cbae7', 'CMP-20260905-0028', 'ATM_MUM_ANDHERI_02', 0.851, 3.1, now() - interval '66 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('042a9462-5dd6-4b01-901a-7383754b88c6', 'CMP-20260905-0018', 'ATM_MUM_ANDHERI_03', 0.737, 1.9, now() - interval '69 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('f30b8efb-87d4-4271-8b2d-4217597adfca', 'CMP-20260905-0020', 'ATM_DEL_CP_05', 0.9, 2.9, now() - interval '72 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        

            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('f9d56180-0550-4003-94ac-b581cbd21cd8', 'CMP-20260905-0019', 'ATM_DEL_CP_03', 0.75, 3.2, now() - interval '75 hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        
DROP TABLE temp_officers;
COMMIT;