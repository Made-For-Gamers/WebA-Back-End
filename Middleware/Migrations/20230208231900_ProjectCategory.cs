using System;
using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace Middleware.Migrations
{
    /// <inheritdoc />
    public partial class ProjectCategory : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Categories",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Engine = table.Column<string>(type: "text", nullable: false),
                    Platforms = table.Column<string>(type: "text", nullable: false),
                    ProgrammingLanguages = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Categories", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Users",
                columns: table => new
                {
                    Id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    UserId = table.Column<Guid>(type: "uuid", nullable: false),
                    Name = table.Column<string>(type: "text", nullable: false),
                    Email = table.Column<string>(type: "text", nullable: false),
                    PasswordHash = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Users", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Projects",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Name = table.Column<string>(type: "text", nullable: false),
                    Description = table.Column<string>(type: "text", nullable: false),
                    CategoryId = table.Column<Guid>(type: "uuid", nullable: false),
                    UserId = table.Column<int>(type: "integer", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Projects", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Projects_Users_UserId",
                        column: x => x.UserId,
                        principalTable: "Users",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "UserClaim",
                columns: table => new
                {
                    Value = table.Column<string>(type: "text", nullable: false),
                    Type = table.Column<string>(type: "text", nullable: false),
                    UserId = table.Column<int>(type: "integer", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_UserClaim", x => x.Value);
                    table.ForeignKey(
                        name: "FK_UserClaim_Users_UserId",
                        column: x => x.UserId,
                        principalTable: "Users",
                        principalColumn: "Id");
                });

            migrationBuilder.InsertData(
                table: "Categories",
                columns: new[] { "Id", "Engine", "Platforms", "ProgrammingLanguages" },
                values: new object[,]
                {
                    { new Guid("2eff621f-4d1b-4014-8d42-5c406f2adb05"), "2", "3", "1" },
                    { new Guid("c03a1b2c-cf79-4750-82a0-fc8e4a829a97"), "1", "0,1,2", "0,2" },
                    { new Guid("cc5adc04-0e95-44e8-8bc9-d51c71c4408e"), "0", "0,1", "0" }
                });

            migrationBuilder.InsertData(
                table: "Users",
                columns: new[] { "Id", "Email", "Name", "PasswordHash", "UserId" },
                values: new object[] { 1, "email@email.email", "name", "fakehash", new Guid("be0a7f8f-e1ba-4fc9-8a44-d0e5f3c4b412") });

            migrationBuilder.InsertData(
                table: "Projects",
                columns: new[] { "Id", "CategoryId", "Description", "Name", "UserId" },
                values: new object[,]
                {
                    { new Guid("4dfedf09-112c-4a37-a58e-5f3e85919928"), new Guid("cc5adc04-0e95-44e8-8bc9-d51c71c4408e"), "Cool test 2", "Test2", 1 },
                    { new Guid("4f8c1258-9046-4bf5-a8cf-57ffdf5504e5"), new Guid("cc5adc04-0e95-44e8-8bc9-d51c71c4408e"), "Cool test", "Test", 1 },
                    { new Guid("6c77e641-6013-42bc-9aba-03bf67be2e5c"), new Guid("c03a1b2c-cf79-4750-82a0-fc8e4a829a97"), "Cool test 3", "Test3", 1 },
                    { new Guid("ed0b541c-5ab5-429f-8ae8-dbe7a4567db8"), new Guid("2eff621f-4d1b-4014-8d42-5c406f2adb05"), "Cool test 4", "Test4", 1 }
                });

            migrationBuilder.CreateIndex(
                name: "IX_Projects_UserId",
                table: "Projects",
                column: "UserId");

            migrationBuilder.CreateIndex(
                name: "IX_UserClaim_UserId",
                table: "UserClaim",
                column: "UserId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Categories");

            migrationBuilder.DropTable(
                name: "Projects");

            migrationBuilder.DropTable(
                name: "UserClaim");

            migrationBuilder.DropTable(
                name: "Users");
        }
    }
}
