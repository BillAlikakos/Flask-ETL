WITH ['C022', 'C002', 'C007', 'C005'] AS arrayParam1, ['C014', 'C004', 'C021'] AS arrayParam2, ['C015', 'C004', 'C021'] AS arrayParam3,
['C014', 'C004', 'C010', 'C018', 'C006', 'C022'] AS arrayParam4, ['C021', 'C003', 'C014', 'C007'] AS arrayParam5,  ['C001', 'C016', 'C003', 'C012'] AS arrayParam6,
['C004', 'C003', 'C010'] AS arrayParam7, ['C016', 'C008', 'C019', 'C002'] AS arrayParam8, ['C001', 'C004', 'C021', 'C010'] AS arrayParam9,
['C012', 'C003'] AS arrayParam10, ['C021', 'C012', 'C019', 'C007'] AS arrayParam11, ['C012', 'C006', 'C020'] AS arrayParam12, ['C019', 'C003', 'C015', 'C012'] AS arrayParam13,
['C001', 'C006', 'C010', 'C019'] AS arrayParam14, ['C010', 'C016', 'C022', 'C020'] AS arrayParam15, ['C016', 'C008', 'C019', 'C002'] AS arrayParam16,
['C022', 'C002', 'C007', 'C005', 'C001', 'C004', 'C021', 'C010'] AS arrayParam17, ['C015', 'C004', 'C021', 'C014', 'C004', 'C010', 'C018', 'C006', 'C022', 'C002', 'C020', 'C009', 'C012'] AS arrayParam18, 
['C002', 'C020', 'C009', 'C012'] AS arrayParam19, ['C016', 'C008', 'C019', 'C002'] AS arrayParam20

CREATE (u1:User {userId: "U001", clotheIDs: arrayParam1})
CREATE (u2:User {userId: "U002", clotheIDs: arrayParam2})
CREATE (u3:User {userId: "U003", clotheIDs: arrayParam3})
CREATE (u4:User {userId: 'U004', clotheIDs: arrayParam4})
CREATE (u5:User {userId: 'U005', clotheIDs: arrayParam5})
CREATE (u6:User {userId: 'U006', clotheIDs: arrayParam6})
CREATE (u7:User {userId: 'U007', clotheIDs: arrayParam7})
CREATE (u8:User {userId: 'U008', clotheIDs: arrayParam8})
CREATE (u9:User {userId: 'U009', clotheIDs: arrayParam9})
CREATE (u10:User {userId: 'U010', clotheIDs: arrayParam10})
CREATE (u11:User {userId: 'U011', clotheIDs: arrayParam11})
CREATE (u12:User {userId: 'U012', clotheIDs: arrayParam12})
CREATE (u13:User {userId: 'U013', clotheIDs: arrayParam13})
CREATE (u14:User {userId: 'U014', clotheIDs: arrayParam14})
CREATE (u15:User {userId: 'U015', clotheIDs: arrayParam15})
CREATE (u16:User {userId: 'U016', clotheIDs: arrayParam16})
CREATE (u17:User {userId: 'U017', clotheIDs: arrayParam17})
CREATE (u18:User {userId: 'U018', clotheIDs: arrayParam18})
CREATE (u19:User {userId: 'U019', clotheIDs: arrayParam19})
CREATE (u20:User {userId: 'U020', clotheIDs: arrayParam20})

CREATE (u1)-[:COLLEAGUE]->(u3)
CREATE (u1)-[:COLLEAGUE]->(u2)
CREATE (u1)-[:COLLEAGUE]->(u20)
CREATE (u1)-[:FRIEND]->(u5)
CREATE (u1)-[:FRIEND]->(u11)
CREATE (u1)-[:FRIEND]->(u13)
CREATE (u1)-[:FRIEND]->(u14)
CREATE (u1)-[:COLLEAGUE]->(u17)

CREATE (u2)-[:FRIEND]->(u3)
CREATE (u2)-[:FRIEND]->(u6)
CREATE (u2)-[:FRIEND]->(u7)
CREATE (u2)-[:FRIEND]->(u15)
CREATE (u2)-[:COLLEAGUE]->(u1)
CREATE (u2)-[:COLLEAGUE]->(u5)
CREATE (u2)-[:COLLEAGUE]->(u11)
CREATE (u2)-[:COLLEAGUE]->(u14)

CREATE (u3)-[:FRIEND]->(u12)
CREATE (u3)-[:FRIEND]->(u18)
CREATE (u3)-[:FRIEND]->(u19)
CREATE (u3)-[:COLLEAGUE]->(u4)
CREATE (u3)-[:COLLEAGUE]->(u1)

CREATE (u4)-[:FRIEND]->(u10)
CREATE (u4)-[:COLLEAGUE]->(u3)
CREATE (u4)-[:COLLEAGUE]->(u18)

CREATE (u5)-[:FRIEND]->(u7)
CREATE (u5)-[:FRIEND]->(u1)
CREATE (u5)-[:COLLEAGUE]->(u2)
CREATE (u5)-[:COLLEAGUE]->(u11)
CREATE (u5)-[:COLLEAGUE]->(u14)

CREATE (u6)-[:FRIEND]->(u2)
CREATE (u6)-[:COLLEAGUE]->(u19)

CREATE (u7)-[:FRIEND]->(u3)
CREATE (u7)-[:FRIEND]->(u5)
CREATE (u7)-[:COLLEAGUE]->(u11)
CREATE (u7)-[:COLLEAGUE]->(u14)

CREATE (u8)-[:FRIEND]->(u20)
CREATE (u8)-[:COLLEAGUE]->(u16)

CREATE (u9)-[:FRIEND]->(u17)
CREATE (u9)-[:COLLEAGUE]->(u10)

CREATE (u10)-[:FRIEND]->(u4)
CREATE (u10)-[:COLLEAGUE]->(u9)

CREATE (u11)-[:FRIEND]->(u1)
CREATE (u11)-[:COLLEAGUE]->(u2)
CREATE (u11)-[:COLLEAGUE]->(u5)

CREATE (u12)-[:FRIEND]->(u3)
CREATE (u12)-[:FRIEND]->(u19)
CREATE (u12)-[:COLLEAGUE]->(u1)

CREATE (u13)-[:FRIEND]->(u1)
CREATE (u13)-[:COLLEAGUE]->(u5)

CREATE (u14)-[:FRIEND]->(u1)
CREATE (u14)-[:COLLEAGUE]->(u2)
CREATE (u14)-[:COLLEAGUE]->(u5)
CREATE (u14)-[:COLLEAGUE]->(u7)

CREATE (u15)-[:FRIEND]->(u2)
CREATE (u15)-[:FRIEND]->(u19)
CREATE (u15)-[:COLLEAGUE]->(u4)

CREATE (u16)-[:FRIEND]->(u20)
CREATE (u16)-[:COLLEAGUE]->(u8)

CREATE (u17)-[:FRIEND]->(u9)
CREATE (u17)-[:COLLEAGUE]->(u1)

CREATE (u18)-[:FRIEND]->(u3)
CREATE (u18)-[:FRIEND]->(u19)
CREATE (u18)-[:COLLEAGUE]->(u4)

CREATE (u19)-[:FRIEND]->(u3)
CREATE (u19)-[:FRIEND]->(u12)
CREATE (u19)-[:FRIEND]->(u15)
CREATE (u19)-[:COLLEAGUE]->(u6)

CREATE (u20)-[:FRIEND]->(u8)
CREATE (u20)-[:FRIEND]->(u16)
CREATE (u20)-[:COLLEAGUE]->(u1)
