class CreateTestExecs < ActiveRecord::Migration
  def change
    create_table :test_execs do |t|
      t.string :uuid
      t.string :name
      t.column :status, :integer

      t.timestamps null: false
    end
  end
end
