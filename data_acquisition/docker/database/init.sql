/*SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
*/
USE 'local-aq';


/* ---- testing
CREATE TABLE IF NOT EXISTS Test (
  Counter int(11) NOT NULL,
  Timestamp timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
*/

CREATE TABLE IF NOT EXISTS iaq (
  Timestamp timestamp NOT NULL DEFAULT current_timestamp(),
  temperature float DEFAULT NULL,
  RH float DEFAULT NULL,
  dew_point float DEFAULT NULL,
  abs_humidity float DEFAULT NULL,
  co2 float DEFAULT NULL,
  voc_index float DEFAULT NULL,
  voc_acc float DEFAULT NULL,
  voc_eq_co2 float DEFAULT NULL,
  luminance float DEFAULT NULL,
  turned_on float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*  testing  */ 
CREATE EVENT IF NOT EXISTS `retention_rate`
  ON SCHEDULE EVERY 1 DAY STARTS '2020-09-01 00:00:00'
  ON COMPLETION PRESERVE
DO DELETE FROM iaq WHERE Timestamp < (NOW() - INTERVAL 1 MONTH);

/*
CREATE EVENT IF NOT EXISTS `retention_rate`
  ON SCHEDULE EVERY 1 DAY STARTS '2020-09-01 00:00:00'
  ON COMPLETION PRESERVE
DO DELETE FROM iaq WHERE Timestamp < (NOW() - INTERVAL 1 MONTH);
*/



/* -- testing
CREATE EVENT IF NOT EXISTS `testEvent`
  ON SCHEDULE EVERY 3 MINUTE STARTS '2020-09-01 00:00:00'
  ON COMPLETION PRESERVE
DO DELETE FROM iaq WHERE Timestamp < (NOW() - INTERVAL 5 MINUTE);


 */

/*SET GLOBAL event_scheduler="ON"*/


