import sqlite3
import os


from flask import Flask, redirect, render_template, request

#STATIC VARIABLES FOR UPLOADING IMAGES
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/pictures')
print(APP_ROOT)
print(UPLOAD_FOLDER)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER




@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST": 
		
		if request.form["Form_Type"] == "Move":		
    
	    # TODO: request all fields from the HTML form (opponent, day, month, location)
			Name = request.form.get("Name")
			#Category = request.form.get("Category")
			Category = request.form.get("Cat_Tag")
			Description = request.form.get("Description")
			Level = request.form.get("Level")
			Invert= request.form.get("Invert")
			Tags = request.form.get("Tags")
			#Creates Consistency over all entries
			Name=Name.title()
			Tags=Tags.title()

			#SAVING IMAGES 
			image = request.files['filename']
			#Image = image.filename			
			#print(Image)
			#this gets the file extension of file uploaded
			fileExt = os.path.splitext(image.filename	)[1]
			print(fileExt)
			if fileExt == ".MOV":
				fileExt=".mp4"
			imgName = Name + fileExt
			image.save(os.path.join(app.config["UPLOAD_FOLDER"],imgName))


			if request.form.get("Category") == "other":
				print ("other")
				print(Category)
				#C_tag = request.form.get("Cat_Tag")
				Category=Category.title()
				with sqlite3.connect('moves.db') as conn:
					cursor = conn.cursor()
					cursor.execute("INSERT INTO cat_tags (cat_tag) VALUES (?)", (Category,))
				#ADD NEW CATEGORY TO CATEGORY TABLE
				
	
			# TODO: create a SQL statement to INSERT event into the database
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO moves (Name, Category, Description, Level, Invert, Image, Tags) VALUES (?, ?, ?, ?, ?, ?, ?)", (Name, Category, Description, Level, Invert, imgName, Tags))
				#cursor.execute("INSERT INTO events (opponent, day, month, location) VALUES (?, ?, ?, ?)", (opponent, day, month, location))

				#ADD ALIAS TO MOVE
				cursor.execute("SELECT id FROM moves WHERE Name=?", (Name,))
				M_id=cursor.fetchall()[0][0]
				print (M_id)
				
			return redirect("/")
		
		
			
		#elif request.form["Form_Type"] == "Upload":
			#image = request.files['filename']
			#image.save(os.path.join(app.config["UPLOAD_FOLDER"], 'hopeful2.jpg'))
			#return redirect("/")
			
		
		elif request.form["Form_Type"] == "Add_To_Sequence":
			print("ADDING TO SEQUENCE")
			S_Name = request.form["Seq_Name"]
			print(S_Name)
			S_Move = request.form.get("S_Move")
			Move_Order = request.form.get("Move_Order")
			#print(S_Move)
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO sequences (S_Name, S_Move, Move_Order) VALUES (?, ?, ?)", (S_Name, S_Move, Move_Order))
			
	#get the moves and sequence moves
			return redirect("/")
		
		
		elif request.form["Form_Type"] == "CreateSequence":
			print("CREATE")
			S_Name = request.form.get("S_Name")
			S_Name=S_Name.title()
			print("SNAME")
			image = request.files['filename']
			print("IMAGE")
			#Image = image.filename			
			#print(Image)
			#this gets the file extension of file uploaded
			fileExt = os.path.splitext(image.filename	)[1]
			#print(fileExt)
			
			imgName = S_Name + fileExt
			image.save(os.path.join(app.config["UPLOAD_FOLDER"],imgName))
			print("INJECT")
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO sequence_storage (S_Name, S_Video) VALUES (?, ?)", (S_Name, imgName))	#Add insert S_Size too
			
			return redirect("/")
			
		elif request.form["Form_Type"] == "Add_Cat_Tag":
			C_tag = request.form.get("Cat_Tag")
			C_tag=C_tag.capitalize()
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO cat_tags (cat_tag) VALUES (?)", (C_tag,))
			return redirect("/")
	#DELETE MOVE
		
	elif request.args.get("id",default="") != "":
    #eventid = ""

		# TODO: get the id from the query string
		id = request.args.get("id")
		with sqlite3.connect('moves.db') as conn:
			cursor = conn.cursor()
			#DELETE THE IMAGE ALONG WITH THE MOVE ENTRY
			cursor.execute("SELECT Image FROM moves WHERE id=?",[id])
			m_name = cursor.fetchall()
			#print(m_name[0][0])
			file = m_name[0][0]
			file = os.path.join(app.config["UPLOAD_FOLDER"],file)
			os.remove(file)
			cursor.execute("DELETE FROM moves WHERE id=?", [id])
		# Connect to database and delete event from the database using the event id	
		
		return redirect("/")

	#DELETE SEQUENCE PART
	elif request.args.get("S_id",default="") != "":
    #eventid = ""

		# TODO: get the id from the query string
		id = request.args.get("S_id")
		with sqlite3.connect('moves.db') as conn:
			cursor = conn.cursor()
			cursor.execute("DELETE FROM sequences WHERE S_id=?", [id])
		# Connect to database and delete event from the database using the event id
			
		
		return redirect("/")
	#DELETE SEQUENCE NAME
	elif request.args.get("Seq_id",default="") != "": 
    #eventid = ""

		# TODO: get the id from the query string
		id = request.args.get("Seq_id")
		with sqlite3.connect('moves.db') as conn:
			cursor = conn.cursor()
			cursor.execute("DELETE FROM sequences WHERE S_Name IN (SELECT sequences.S_Name FROM sequences INNER JOIN sequence_storage on sequences.S_Name = sequence_storage.S_Name WHERE sequence_storage.S_id=?)", [id])
			cursor.execute("DELETE FROM sequence_storage WHERE S_id=?", [id])
			
		# Connect to database and delete event from the database using the event id
			
		
		return redirect("/")	
			
#TEST FOR HAVING LINKS TO PAGES ABOUT MOVES	
	elif request.args.get("entry_id",default="") != "":
			id = request.args.get("entry_id")
			M_Name=request.args.get("M_Name")
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("SELECT E_Image FROM entries WHERE E_id=?",[id])
				m_name = cursor.fetchall()
				file = m_name[0][0]
				file = os.path.join(app.config["UPLOAD_FOLDER"],file)
				os.remove(file)
				cursor.execute("DELETE FROM entries WHERE E_id=?", [id])
			# Connect to database and delete event from the database using the event id
				
			
			return Move(M_Name)
	elif request.args.get("S_Name",default="") != "":
		S_Name=request.args.get("S_Name")
		return viewSeq(S_Name)
	elif request.args.get("M_Name",default="") != "":
    #eventid = ""

		# TODO: get the id from the query string
		M_Name = request.args.get("M_Name")
		return Move(M_Name)
			
	#DELETE ALIAS	
	elif request.args.get("alias_name",default="") != "":
    #eventid = ""
		
		# TODO: get the id from the query string
		alias = request.args.get("alias_name")
		M_Name = request.args.get("name")
		#print(alias)
		with sqlite3.connect('moves.db') as conn:
			cursor = conn.cursor()		
			cursor.execute("DELETE FROM move_alias WHERE alias=?", [alias])		
		return Move(M_Name)
		
	elif request.args.get("Search",default="") != "":
			print("SEARCH")
			#Creates new table everytime its called
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("DROP TABLE search")
				#cursor.execute("CREATE TABLE search (id INTEGER, Name varchar(200), Category varchar(200), Description varchar(200), Level INTEGER, Invert varchar(5))")
				cursor.execute("CREATE TABLE search (id INTEGER, Name varchar(200), alias varchar(200))")
			#Gets value put into the search box
			Search_Val = request.args.get("Search")
			#print(Search_Val)
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				#cursor.execute("SELECT Name, Category, Description, Level, Invert FROM moves WHERE Name LIKE ? OR Category LIKE ? OR Description LIKE ?",("%"+Search_Val + "%","%"+Search_Val  + "%", "%"+Search_Val + "%"))
				cursor.execute("SELECT Name FROM moves WHERE Name LIKE ? OR Category LIKE ? OR Description LIKE ? OR Tags LIKE ?",("%"+Search_Val + "%","%"+Search_Val  + "%", "%"+Search_Val + "%", "%"+Search_Val + "%"))
				searched_rows=cursor.fetchall()
				#allows user to search by alias as well
				cursor.execute("SELECT Name FROM moves INNER JOIN move_alias ON moves.Name = move_alias.m_name WHERE Name LIKE ? OR move_alias.alias LIKE ? GROUP BY Name",("%"+Search_Val + "%","%"+Search_Val  + "%"))
				# OR move_alias.alias LIKE ?
				
				alias_rows=cursor.fetchall()
				#print(test_rows)
				#print("test_rows")
				for rows in searched_rows:
					print(rows)
					print("row")					
					cursor.execute("INSERT INTO search (Name) VALUES(?)", (rows))
				for rows in alias_rows:
					print(rows)
					print("row")					
					cursor.execute("INSERT INTO search (Name) VALUES(?)", (rows))
				#print(cursor.fetchall())
				
			
			
					
			return redirect("/")
	elif request.args.get("back",default="") !="":
			print("go back")
			return redirect("/")
	
	
	
	
	
	
	else:		
		# TODO: Query the database events.db and select all records from event table
		
			

		with sqlite3.connect('moves.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			cursor.execute("SELECT id, Name, Category, Description, Level, Invert, Image FROM moves ORDER BY Level, Category, Name")
			moves_rows = (cursor.fetchall())
			

		#with sqlite3.connect('moves.db') as conn:
			#conn.row_factory = sqlite3.Row
			#cursor = conn.cursor()
			#cursor.execute("SELECT S_id, S_Name, S_Move, Move_Order FROM sequences ORDER BY S_Name, Move_Order ASC")
			#sequence_rows = (cursor.fetchall())

		with sqlite3.connect('moves.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			#cursor.execute("SELECT sequence_storage.S_Name, GROUP_CONCAT( sequences.S_Move||':'||sequences.Move_Order||':'||sequences.S_id, ','), sequence_storage.S_id, moves.Image FROM sequence_storage INNER JOIN sequences on sequences.S_Name = sequence_storage.S_Name INNER JOIN moves ON moves.Name = sequences.S_Move GROUP BY sequence_storage.S_Name")

			cursor.execute("SELECT sequence_storage.S_Name, GROUP_CONCAT( sequences.S_Move||':'||sequences.Move_Order||':'||sequences.S_id, ','), sequences.S_Name,  sequence_storage.S_id FROM sequence_storage LEFT JOIN sequences on sequence_storage.S_Name = sequences.S_Name  GROUP BY sequence_storage.S_Name")
										 
										 
			sequence_rows = (cursor.fetchall())
			
				
		with sqlite3.connect('moves.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			cursor.execute("SELECT S_id, S_Name FROM sequence_storage")
			S_Name_rows = (cursor.fetchall())
			
		with sqlite3.connect('moves.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			#cursor.execute("SELECT id, Name, Category, Description, Level, Invert FROM search ORDER BY Level, Name")
			cursor.execute("SELECT id, Name FROM search GROUP BY Name ORDER BY Name")
			search_rows = (cursor.fetchall())
			#print(search_rows)
		
		with sqlite3.connect('moves.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			cursor.execute("SELECT cat_tag FROM cat_tags")
			cat_rows = (cursor.fetchall())
		#	test_rows =""
		#	for name in S_Name_rows:
				#print("Hi")
		#		print(name["S_Name"])
		#		with sqlite3.connect('moves.db') as conn:
		#			conn.row_factory = sqlite3.Row
		#			cursor = conn.cursor()
		#			cursor.execute("SELECT S_Move, Move_Order FROM sequences WHERE S_Name = ? ORDER BY Move_Order ASC", (name["S_Name"],))
		#			test_rows = (cursor.fetchall())
					#print(test_rows)
		#			for val in test_rows:
		#				print(val["S_Move"])
		
			
			#cursor.execute("SELECT id, Name, Category, Description, Level, Invert FROM moves WHERE Name = ?", [search])
			#search_rows = (cursor.fetchall())
			
			
		
		# TODO: add a parameter pass events to the HTML template
		
		return render_template("index.html", moves=moves_rows, sequences=sequence_rows, sequence_names=S_Name_rows, search=search_rows, categories=cat_rows)





@app.route("/EditSeq.html", methods=["GET", "POST"])
def EditSeq():
	if request.method =="POST":
		if request.form["Form_Type"] == "Go_Back":
			return redirect("/")
		elif request.form["Form_Type"] == "Add_To_Sequence":
			print("ADDING TO SEQUENCE 2")
			S_Name = request.form["Seq_Name"]
			#print(S_Name)
			S_Move = request.form.get("S_Move")
			Move_Order = request.form.get("Move_Order")
			#print(S_Move)
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO sequences (S_Name, S_Move, Move_Order) VALUES (?, ?, ?)", (S_Name, S_Move, Move_Order))
			
	#get the moves and sequence moves
			#return redirect("/EditSeq.html")	
		elif request.form["Form_Type"] == "Edit_Sequence":
			print("EDIT SEQUENCE 2")
			S_Name = request.form.get("Edit_S")
			#print(S_Name)
		
	elif request.args.get("S_id",default="") != "":
    #eventid = ""

		# TODO: get the id from the query string
		id = request.args.get("S_id")
		with sqlite3.connect('moves.db') as conn:
			cursor = conn.cursor()
			cursor.execute("SELECT S_Name FROM sequences WHERE S_id=?", [id])
			Result=(cursor.fetchall())
			S_Name=Result[0][0]
			#print(S_Name)
			cursor.execute("DELETE FROM sequences WHERE S_id=?", [id])
		# Connect to database and delete event from the database using the event id		
	return viewSeq(S_Name)
		
	

	
	
	
	
def viewSeq(S_Name):
# This is needed for every function to render the page 
	with sqlite3.connect('moves.db') as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT id, Name, Category, Description, Level, Invert FROM moves ORDER BY Level, Category, Name")
		moves_rows = (cursor.fetchall())
		
	with sqlite3.connect('moves.db') as conn:
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("SELECT S_id, S_Name, S_Move, Move_Order, moves.Image FROM sequences INNER JOIN moves ON moves.Name = sequences.S_Move WHERE S_Name = ? ORDER BY S_Name, Move_Order ASC", (S_Name,))
		#cursor.execute("SELECT DISTINCT Move_Order, S_Name FROM sequences WHERE S_Name = ? ORDER BY Move_Order ASC", (S_Name,))
		#print(cursor.fetchall())
		sequence_rows = (cursor.fetchall())
		#print(sequence_rows)
		
#return redirect("EditSeq.html")	
	#return redirect("EditSeq.html")
	
	return render_template("EditSeq.html", S_Name=S_Name, moves=moves_rows, sequences=sequence_rows)

		
	
		
	

@app.route("/Move.html", methods=["GET", "POST"])
def EditMove():
	
	if request.form["Form_Type"] == "Go_Back":
			return redirect("/")
	elif request.form["Form_Type"] == "Add_Alias":
		alias=request.form.get("Alias").capitalize()
		M_Name = request.form.get("M_Name")
		#print(M_Name)
		with sqlite3.connect('moves.db') as conn:
			cursor = conn.cursor()
			cursor.execute("INSERT INTO move_alias (m_name, alias) VALUES (?,?)", (M_Name, alias))
			#display rows
			cursor.execute("SELECT * FROM moves WHERE Name=?", [M_Name])
			move_rows=(cursor.fetchall())
			cursor.execute("SELECT alias FROM move_alias WHERE m_name=?", [M_Name])
			alias_rows=(cursor.fetchall())
		return render_template("Move.html", move_info=move_rows, alias_info=alias_rows) 

	
	
			
	
	elif request.form["Form_Type"] == "Add_Entry":		
    
	    # TODO: request all fields from the HTML form (opponent, day, month, location)
			Name = request.form.get("Entry_Name")
			Category = request.form.get("Entry_Category")
			Description = request.form.get("Entry_Description")
			Level = request.form.get("Entry_Level")
			Invert= request.form.get("Entry_Invert")
			M_Name=request.form.get("M_Name")
			#Creates Consistency over all entries
			Name=Name.capitalize()

			#SAVING IMAGES 
			image = request.files['filename']
			#Image = image.filename			
			#print(Image)
			#this gets the file extension of file uploaded
			fileExt = os.path.splitext(image.filename	)[1]
			#print(fileExt)
			if fileExt == ".jpg" and Description != "Pose":
				print("Incompatable")
				return render_template("Error.html")
			imgName = Name + fileExt
			image.save(os.path.join(app.config["UPLOAD_FOLDER"],imgName))


			
	
			# TODO: create a SQL statement to INSERT event into the database
			with sqlite3.connect('moves.db') as conn:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO entries (E_Name, E_Category, E_Description, E_Level, E_Invert, E_Image, base_move) VALUES (?, ?, ?, ?, ?, ?, ?)", (Name, Category, Description, Level, Invert, imgName, M_Name))
				#cursor.execute("INSERT INTO events (opponent, day, month, location) VALUES (?, ?, ?, ?)", (opponent, day, month, location))

				
				
			#return redirect("/")
		
		
				
		
	else:	
		M_Name = request.args.get("M_Name")
	#DISPLAY MOVE INFO
	return Move(M_Name)

def Move(M_Name):
	print(M_Name)
	with sqlite3.connect('moves.db') as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM moves WHERE Name=?", [M_Name])
		move_rows=(cursor.fetchall())
		print(move_rows)
		cursor.execute("SELECT alias FROM move_alias WHERE m_name=?", [M_Name])
		alias_rows=(cursor.fetchall())
		
		cursor.execute("SELECT * FROM entries WHERE base_move=?", [M_Name])
		entry_rows=(cursor.fetchall())
		print("ENTRY")
		print("entry_rows")

		cursor.execute("SELECT cat_tag FROM cat_tags")
		cat_tag_rows=(cursor.fetchall())
		#print("CAT ROWS") 
		#print(cat_tag_rows)
		
	return render_template("Move.html", move_info=move_rows, alias_info=alias_rows,entries=entry_rows, categories=cat_tag_rows)
@app.route("/Error.html", methods=["GET", "POST"])
def Error():
	if request.form["Form_Type"] == "Go_Back":
			return redirect("/")
	return render_template("Error.html")
	

@app.errorhandler(sqlite3.IntegrityError)
def handle_bad_input(e):
	print("INVALID INPUT")
	return render_template("Error.html")
		
app.run(host='0.0.0.0', port=8080)
