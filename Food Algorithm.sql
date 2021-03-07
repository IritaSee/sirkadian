-- app.py migrate
-- app.py revision -m first_init
-- paste this on upgrade()
-- op.execute("""
INSERT INTO `sirkadian`.`food_max` (`id`) VALUES ('1');
SELECT MAX(calorie) FROM food INTO @max_calorie;
SELECT MAX(protein) FROM food INTO @max_protein;
SELECT MAX(fat) FROM food INTO @max_fat;
SELECT MAX(carbohydrate) FROM food INTO @max_carbohydrate;
SELECT MAX(fiber) FROM food INTO @max_fiber;
SELECT MAX(calcium) FROM food INTO @max_calcium;
SELECT MAX(phosphor) FROM food INTO @max_phosphor;
SELECT MAX(iron) FROM food INTO @max_iron;
SELECT MAX(sodium) FROM food INTO @max_sodium;
SELECT MAX(potassium) FROM food INTO @max_potassium;
SELECT MAX(copper) FROM food INTO @max_copper;
SELECT MAX(zinc) FROM food INTO @max_zinc;
SELECT MAX(vit_a) FROM food INTO @max_vit_a;
SELECT MAX(vit_b1) FROM food INTO @max_vit_b1;
SELECT MAX(vit_b2) FROM food INTO @max_vit_b2;
SELECT MAX(vit_b3) FROM food INTO @max_vit_b3;
SELECT MAX(vit_c) FROM food INTO @max_vit_c;

UPDATE food_max
SET
	max_calorie = @max_calorie,
	max_protein = @max_protein,
	max_fat = @max_fat,
	max_carbohydrate = @max_carbohydrate,
	max_fiber = @max_fiber,
	max_calcium = @max_calcium,
	max_phosphor = @max_phosphor,
	max_iron = @max_iron,
	max_sodium = @max_sodium,
	max_potassium = @max_potassium,
	max_copper = @max_copper,
	max_zinc = @max_zinc,
	max_vit_a = @max_vit_a,
	max_vit_b1 = @max_vit_b1,
	max_vit_b2 = @max_vit_b2,
	max_vit_b3 = @max_vit_b3,
	max_vit_c = @max_vit_c
	;

UPDATE food
SET nutri_point=(((calorie/@max_calorie)+(protein/@max_protein)+(fat/@max_fat)+(carbohydrate/@max_carbohydrate)+(fiber/@max_fiber)+(calcium/@max_calcium)+(phosphor/@max_phosphor)+(iron/@max_iron)+(sodium/@max_sodium)+(potassium/@max_potassium)+(copper/@max_copper)+(zinc/@max_zinc)+(vit_a/@max_vit_a)+(vit_b1/@max_vit_b1)+(vit_b2/@max_vit_b2)+(vit_b3/@max_vit_b3)+(vit_c/@max_vit_c))*100/17);
SET @food_need_update := 0;

-- HAPUS DELIMITER //
DELIMITER //
CREATE TRIGGER before_food_helper_insert
BEFORE INSERT
ON food_helper FOR EACH ROW
BEGIN
IF @food_max_updated = 1 THEN
	SET @food_need_updated := 0;
	IF NEW.calorie > @max_calorie THEN
		SET @max_calorie = NEW.calorie;
		SET @food_need_update := 1;
	END IF;
	IF NEW.protein > @max_protein THEN
		SET @max_protein = NEW.protein;
		SET @food_need_update := 1;
	END IF;
	IF NEW.fat > @max_fat THEN
		SET @max_fat = NEW.fat;
		SET @food_need_update := 1;
	END IF;
	IF NEW.carbohydrate > @max_carbohydrate THEN
		SET @max_carbohydrate = NEW.carbohydrate;
		SET @food_need_update := 1;
	END IF;
	IF NEW.fiber > @max_fiber THEN
		SET @max_fiber = NEW.fiber;
		SET @food_need_update := 1;
	END IF;
	IF NEW.calcium > @max_calcium THEN
		SET @max_calcium = NEW.calcium;
		SET @food_need_update := 1;
	END IF;
	IF NEW.phosphor > @max_phosphor THEN
		SET @max_phosphor = NEW.phosphor;
		SET @food_need_update := 1;
	END IF;
	IF NEW.iron > @max_iron THEN
		SET @max_iron = NEW.iron;
		SET @food_need_update := 1;
	END IF;
	IF NEW.sodium > @max_sodium THEN
		SET @max_sodium = NEW.sodium;
		SET @food_need_update := 1;
	END IF;
	IF NEW.potassium > @max_potassium THEN
		SET @max_potassium = NEW.potassium;
		SET @food_need_update := 1;
	END IF;
	IF NEW.copper > @max_copper THEN
		SET @max_copper = NEW.copper;
		SET @food_need_update := 1;
	END IF;
	IF NEW.zinc > @max_zinc THEN
		SET @max_zinc = NEW.zinc;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_a > @max_vit_a THEN
		SET @max_vit_a = NEW.vit_a;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_b1 > @max_vit_b1 THEN
		SET @max_vit_b1 = NEW.vit_b1;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_b2 > @max_vit_b2 THEN
		SET @max_vit_b2 = NEW.vit_b2;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_b3 > @max_vit_b3 THEN
		SET @max_vit_b3 = NEW.vit_b3;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_c > @max_vit_c THEN
		SET @max_vit_c = NEW.vit_c;
		SET @food_need_update := 1;
	END IF;

ELSE
	SELECT max_calorie FROM food_max INTO @max_calorie;
	SELECT max_protein FROM food_max INTO @max_protein;
	SELECT max_fat FROM food_max INTO @max_fat;
	SELECT max_carbohydrate FROM food_max INTO @max_carbohydrate;
	SELECT max_fiber FROM food_max INTO @max_fiber;
	SELECT max_calcium FROM food_max INTO @max_calcium;
	SELECT max_phosphor FROM food_max INTO @max_phosphor;
	SELECT max_iron FROM food_max INTO @max_iron;
	SELECT max_sodium FROM food_max INTO @max_sodium;
	SELECT max_potassium FROM food_max INTO @max_potassium;
	SELECT max_copper FROM food_max INTO @max_copper;
	SELECT max_zinc FROM food_max INTO @max_zinc;
	SELECT max_vit_a FROM food_max INTO @max_vit_a;
	SELECT max_vit_b1 FROM food_max INTO @max_vit_b1;
	SELECT max_vit_b2 FROM food_max INTO @max_vit_b2;
	SELECT max_vit_b3 FROM food_max INTO @max_vit_b3;
	SELECT max_vit_c FROM food_max INTO @max_vit_c;

	SET @food_max_updated := 1;
	SET @food_need_updated := 0;

	IF NEW.calorie > @max_calorie THEN
		SET @max_calorie = NEW.calorie;
		SET @food_need_update := 1;
	END IF;
	IF NEW.protein > @max_protein THEN
		SET @max_protein = NEW.protein;
		SET @food_need_update := 1;
	END IF;
	IF NEW.fat > @max_fat THEN
		SET @max_fat = NEW.fat;
		SET @food_need_update := 1;
	END IF;
	IF NEW.carbohydrate > @max_carbohydrate THEN
		SET @max_carbohydrate = NEW.carbohydrate;
		SET @food_need_update := 1;
	END IF;
	IF NEW.fiber > @max_fiber THEN
		SET @max_fiber = NEW.fiber;
		SET @food_need_update := 1;
	END IF;
	IF NEW.calcium > @max_calcium THEN
		SET @max_calcium = NEW.calcium;
		SET @food_need_update := 1;
	END IF;
	IF NEW.phosphor > @max_phosphor THEN
		SET @max_phosphor = NEW.phosphor;
		SET @food_need_update := 1;
	END IF;
	IF NEW.iron > @max_iron THEN
		SET @max_iron = NEW.iron;
		SET @food_need_update := 1;
	END IF;
	IF NEW.sodium > @max_sodium THEN
		SET @max_sodium = NEW.sodium;
		SET @food_need_update := 1;
	END IF;
	IF NEW.potassium > @max_potassium THEN
		SET @max_potassium = NEW.potassium;
		SET @food_need_update := 1;
	END IF;
	IF NEW.copper > @max_copper THEN
		SET @max_copper = NEW.copper;
		SET @food_need_update := 1;
	END IF;
	IF NEW.zinc > @max_zinc THEN
		SET @max_zinc = NEW.zinc;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_a > @max_vit_a THEN
		SET @max_vit_a = NEW.vit_a;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_b1 > @max_vit_b1 THEN
		SET @max_vit_b1 = NEW.vit_b1;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_b2 > @max_vit_b2 THEN
		SET @max_vit_b2 = NEW.vit_b2;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_b3 > @max_vit_b3 THEN
		SET @max_vit_b3 = NEW.vit_b3;
		SET @food_need_update := 1;
	END IF;
	IF NEW.vit_c > @max_vit_c THEN
		SET @max_vit_c = NEW.vit_c;
		SET @food_need_update := 1;
	END IF;
END IF;
IF @food_need_update = 1 THEN
	INSERT INTO food VALUE(NULL,NEW.name,NEW.food_type,NEW.duration,NEW.serving,NEW.difficulty,NEW.calorie,NEW.protein,NEW.fat,NEW.carbohydrate,NEW.fiber,NEW.calcium,NEW.phosphor,NEW.iron,NEW.sodium,NEW.potassium,NEW.copper,NEW.zinc,NEW.vit_a,NEW.vit_b1,NEW.vit_b2,NEW.vit_b3,NEW.vit_c,NEW.tags,NEW.image_filename,NULL,NULL);
	UPDATE food_max
	SET
		max_calorie = @max_calorie,
		max_protein = @max_protein,
		max_fat = @max_fat,
		max_carbohydrate = @max_carbohydrate,
		max_fiber = @max_fiber,
		max_calcium = @max_calcium,
		max_phosphor = @max_phosphor,
		max_iron = @max_iron,
		max_sodium = @max_sodium,
		max_potassium = @max_potassium,
		max_copper = @max_copper,
		max_zinc = @max_zinc,
		max_vit_a = @max_vit_a,
		max_vit_b1 = @max_vit_b1,
		max_vit_b2 = @max_vit_b2,
		max_vit_b3 = @max_vit_b3,
		max_vit_c = @max_vit_c
		;
	SET @food_need_update := 0;
ELSE
	INSERT INTO food VALUE(NULL,NEW.name,NEW.food_type,NEW.duration,NEW.serving,NEW.difficulty,NEW.calorie,NEW.protein,NEW.fat,NEW.carbohydrate,NEW.fiber,NEW.calcium,NEW.phosphor,NEW.iron,NEW.sodium,NEW.potassium,NEW.copper,NEW.zinc,NEW.vit_a,NEW.vit_b1,NEW.vit_b2,NEW.vit_b3,NEW.vit_c,NEW.tags,NEW.image_filename,(((calorie/@max_calorie)+(protein/@max_protein)+(fat/@max_fat)+(carbohydrate/@max_carbohydrate)+(fiber/@max_fiber)+(calcium/@max_calcium)+(phosphor/@max_phosphor)+(iron/@max_iron)+(sodium/@max_sodium)+(potassium/@max_potassium)+(copper/@max_copper)+(zinc/@max_zinc)+(vit_a/@max_vit_a)+(vit_b1/@max_vit_b1)+(vit_b2/@max_vit_b2)+(vit_b3/@max_vit_b3)+(vit_c/@max_vit_c))*100/17),NULL);
END IF;
END//
-- insert coma(,) after END

-- HAPUS DELIMITER //
DELIMITER //
CREATE TRIGGER before_food_max_update
BEFORE UPDATE
ON food_max FOR EACH ROW
BEGIN
SET @max_calorie = NEW.max_calorie;
SET @max_protein = NEW.max_protein;
SET @max_fat = NEW.max_fat;
SET @max_carbohydrate = NEW.max_carbohydrate;
SET @max_fiber = NEW.max_fiber;
SET @max_calcium = NEW.max_calcium;
SET @max_phosphor = NEW.max_phosphor;
SET @max_iron = NEW.max_iron;
SET @max_sodium = NEW.max_sodium;
SET @max_potassium = NEW.max_potassium;
SET @max_copper = NEW.max_copper;
SET @max_zinc = NEW.max_zinc;
SET @max_vit_a = NEW.max_vit_a;
SET @max_vit_b1 = NEW.max_vit_b1;
SET @max_vit_b2 = NEW.max_vit_b2;
SET @max_vit_b3 = NEW.max_vit_b3;
SET @max_vit_c = NEW.max_vit_c;

UPDATE food
SET nutri_point=(((calorie/NEW.max_calorie)+(protein/NEW.max_protein)+(fat/NEW.max_fat)+(carbohydrate/NEW.max_carbohydrate)+(fiber/NEW.max_fiber)+(calcium/NEW.max_calcium)+(phosphor/NEW.max_phosphor)+(iron/NEW.max_iron)+(sodium/NEW.max_sodium)+(potassium/NEW.max_potassium)+(copper/NEW.max_copper)+(zinc/NEW.max_zinc)+(vit_a/NEW.max_vit_a)+(vit_b1/NEW.max_vit_b1)+(vit_b2/NEW.max_vit_b2)+(vit_b3/NEW.max_vit_b3)+(vit_c/NEW.max_vit_c))*100/17);
SET @food_need_update := 0;
END//
-- insert coma(,) after END
-- """)