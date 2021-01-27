-- SQLサンプル
SELECT
  NOW() AS '算出時刻'
  , CASE test_flg
    WHEN '0' THEN '有効(未退会)'
    WHEN '1' THEN '無効(退会)'
    END AS '会員状態'
  , COUNT(*) AS '件数'
FROM
  test
GROUP BY
  test.test_flg;


